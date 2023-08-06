#!/usr/bin/env python
'''Snapshot all public GitHub repos for specified orgs to S3'''
# Requires python 2 for codekit.
# Requires github3 v1.0 for repository iteration.
from __future__ import print_function
import argparse
import os
import os.path
import sys
import datetime
import subprocess
import github3
import progressbar
from codekit import codetools
from .arg_defaulter import add_defaults


class ReportRepo(object):
    '''Class to provide progressbar widget with current repo name.'''

    _current_repo = ''
    _max_length = 0

    def __init__(self):
        pass

    def __call__(self, progress, data):
        return self._current_repo.ljust(self._max_length)

    def set_current_repo(self, arg):
        '''Set current repo name'''
        self._current_repo = arg

    def get_current_repo(self):
        '''Get current repo name'''
        return self._current_repo

    def set_max_length(self, mlen):
        '''Set maximum length of org+repo'''
        self._max_length = mlen

    def get_max_length(self):
        '''Get maximum length of org+repo'''
        return self._max_length


def parse_args():
    '''Parse command-line arguments'''
    parser = argparse.ArgumentParser(
        description="Clone repositories in LSST orgs")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="enable debugging")
    parser.add_argument("-o", "--organizations",
                        help="comma-separated list of organizations" +
                        " [ $GITHUB_ORGS | lsst,lsst-sqre,lsst-dm ]")
    parser.add_argument("-a", "--access-key", "--aws-access-key",
                        "--aws-access-key-id",
                        help="AWS access key ID [ $AWS_ACCESS_KEY_ID | " +
                        "<from instance metadata> ]")
    parser.add_argument("-s", "--secret-access-key", "--aws-secret-access-key",
                        "--secret-key", "--aws-secret-key",
                        help="AWS secret key [ $AWS_SECRET_ACCESS_KEY | " +
                        "<from instance metadata> ]")
    parser.add_argument("-r", "--region", "--default-region",
                        "--aws-default-region",
                        help="AWS default region [ $AWS_DEFAULT_REGION | " +
                        "us-west-2 ]")
    parser.add_argument("-b", "--bucket", "--s3-bucket",
                        help="S3 bucket for storage snapshot" +
                        "[ $S3_BACKUP_BUCKET | lsst-github-backups ]")
    parser.add_argument("-t", "--token", "--github-token",
                        help="GitHub auth token [ $GITHUB_TOKEN ]")
    parser.add_argument("-tf", "--token-file", "--github-token-file",
                        help="Github token file [ if no token literal," +
                        " ~/.sq_github_token ]")
    # LFS support is currently pretty broken; the authentication model is
    #  sort of horrible.
    parser.add_argument("-l", "--lfs", help="Enable fetching LFS objects " +
                        "(experimental)", action="store_true")
    # parser.add_argument("-td", "--tmpdir", "--tmpdir-root",
    #                    help="root directory for temporary storage" +
    #                    " [system default]")
    # codekit.TempDir() needs updating to recognize its root directory.
    results = parser.parse_args()
    if not results.organizations:
        results.organizations = add_defaults("GITHUB_ORGS",
                                             "lsst,lsst-sqre,lsst-dm")
    results.organizations = results.organizations.split(',')
    if not results.access_key:
        results.access_key = add_defaults("AWS_ACCESS_KEY_ID")
    if not results.secret_access_key:
        results.secret_access_key = add_defaults("AWS_SECRET_ACCESS_KEY")
    if not results.region:
        results.region = add_defaults("AWS_DEFAULT_REGION")
        if not results.region:
            results.region = "us-west-2"
    if not results.bucket:
        results.bucket = add_defaults("S3_BACKUP_BUCKET",
                                      "lsst-github-backups")
    if not results.token:
        results.token = add_defaults("GITHUB_TOKEN")
    if not results.token:
        if not results.token_file:
            results.token_file = os.path.expanduser('~/.sq_github_token')
            try:
                with open(results.token_file) as fdc:
                    results.token = fdc.readline().strip()
            except IOError as exc:
                print(exc)
    return results


def backup_repos(args):
    '''Back up repositories'''
    retval = True
    session = None
    if "token" in args and args.token:
        session = codetools.login_github(token=args.token)
    else:
        session = github3.github.GitHub()  # Unauthenticated, probably
        #  will hit rate-limit.
    cloneurls = get_clone_urls(session, args)
    repocount = 0
    for oname in cloneurls:
        repocount += len(cloneurls[oname])
    maxlength = get_reponamelen(cloneurls)

    reporep = ReportRepo()
    reporep.set_max_length(maxlength)
    pbar = progressbar.ProgressBar(
        widgets=[reporep, ' | ', progressbar.ETA(), ' ', progressbar.Bar()],
        max_value=repocount).start()
    urlcount = 0

    for org in cloneurls:
        for url in cloneurls[org]:
            rname = url.split('/')[-1][:-4]
            reporep.set_current_repo(org + "/" + rname)
            urlcount += 1
            pbar.update(urlcount)
            with codetools.TempDir() as tempdir:
                retcode = clone_repo(url, tempdir, lfs=args.lfs)
                if retcode is False:
                    retval = False
                retcode = stash_repo(args, org, tempdir)
                if retcode is None or retcode != 0:
                    retval = False
    return retval


def get_reponamelen(urls):
    '''Determine maximum length of org+repo name'''
    maxlength = 0
    for oname in urls:
        for nnm in urls[oname]:
            rname = nnm.split('/')[-1][:-4]
            nmlen = 1 + len(oname) + len(rname)
            if nmlen > maxlength:
                maxlength = nmlen
    return maxlength


def clone_repo(url, tempdir, lfs=False):
    '''Clone repository from URL'''
    env = os.environ.copy()
    fnull = open(os.devnull, 'w')
    rname = url.split('/')[-1]
    wdir = tempdir + "/" + rname
    cmd = ["git", "clone", "-q", "--mirror", url, wdir]
    sp1 = subprocess.Popen(cmd, env=env, stdin=fnull, stdout=fnull)
    # Keep stderr.
    sp1.wait()
    if lfs:
        cmd2 = ["git", "lfs", "fetch", "--all"]
        sp2 = subprocess.Popen(cmd2, env=env, stdin=fnull, stdout=fnull,
                               cwd=wdir)
        sp2.wait()
        if sp1.returncode == 0:
            return sp2.returncode
    return sp1.returncode


def stash_repo(args, org, tempdir):
    '''Store repository snapshot'''
    # Eventually we'd like to store this with Nebula.
    return stash_repo_amz(args, org, tempdir)


def stash_repo_amz(args, org, tempdir):
    '''Store repository snapshot in S3'''
    # We could do this with boto rather than subprocess, but then we'd
    #  have to implement our own recursive upload method.
    env = os.environ.copy()
    #
    # If these aren't set, the AWS CLI may be able to figure it out
    #  anyway, if we happen to be running from an instance with an
    #  appropriate IAM role set.  See
    #  https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/\
    #   iam-roles-for-amazon-ec2.html#instance-metadata-security-credentials
    #
    if "access_key" in args and args.access_key:
        env["AWS_ACCESS_KEY_ID"] = args.access_key
    if "secret_access_key" in args and args.secret_access_key:
        env["AWS_SECRET_ACCESS_KEY"] = args.secret_access_key
    region = args.region
    env["AWS_DEFAULT_REGION"] = region
    datestr = datetime.date.today().isoformat()
    bucket = "s3://%s/%s/%s/" % (args.bucket, datestr, org)
    fnull = open(os.devnull, 'w')
    cmd = ["aws", "s3", "cp", tempdir + "/", bucket, "--recursive"]
    sp1 = subprocess.Popen(cmd, env=env, stdin=fnull, stdout=fnull)
    # Keep stderr.
    sp1.wait()
    return sp1.returncode


def get_clone_urls(session, args):
    '''Get clone URLs for repositories'''
    cloneurls = {}
    for orgname in args.organizations:
        org = session.organization(orgname)
        cloneurls[orgname] = []
        for repo in org.repositories():
            # Skip private repos
            if not repo.private:
                cloneurls[orgname].append(repo.clone_url)
    return cloneurls


def main():
    '''Main entry point'''
    args = parse_args()
    retval = backup_repos(args)
    if not retval:
        sys.exit(1)

if __name__ == "__main__":
    main()
