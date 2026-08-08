#!/usr/bin/env python3
"""Snapshot public GitHub metrics. GoatCounter aggregates should be exported separately and joined by month."""
from __future__ import annotations
import argparse, datetime as dt, json, os, pathlib, urllib.request

def get(url, token=None):
    h={'Accept':'application/vnd.github+json','User-Agent':'ai-playgrounds-metrics-snapshot'}
    if token: h['Authorization']='Bearer '+token
    with urllib.request.urlopen(urllib.request.Request(url,headers=h),timeout=30) as r: return json.load(r)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--repo',default='lmdixon23/ai-playgrounds'); ap.add_argument('--output',default='metrics/snapshots'); a=ap.parse_args()
    token=os.getenv('GITHUB_TOKEN'); base='https://api.github.com/repos/'+a.repo
    repo=get(base,token); releases=get(base+'/releases',token)
    payload={'captured_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'repository':a.repo,'stars':repo['stargazers_count'],
             'forks':repo['forks_count'],'open_issues':repo['open_issues_count'],'subscribers':repo.get('subscribers_count'),
             'release_assets':[{'tag':r['tag_name'],'assets':[{'name':x['name'],'downloads':x['download_count']} for x in r['assets']]} for r in releases]}
    out=pathlib.Path(a.output); out.mkdir(parents=True,exist_ok=True); p=out/(dt.date.today().isoformat()+'.json'); p.write_text(json.dumps(payload,indent=2),encoding='utf-8'); print(p)
if __name__=='__main__': main()
