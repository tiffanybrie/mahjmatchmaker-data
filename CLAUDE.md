# You are on `main`. The working branch is `partner-catalogs-sqsp`: get it THIS way (Nov 22 2026)

`main` only holds the old Match Builder data. Every rule, script, config and doc (the real CLAUDE.md, scripts/, config/, docs/)
lives on branch `partner-catalogs-sqsp`, which is about 8 GB checked out. A plain `git fetch origin partner-catalogs-sqsp`
(any depth) or a full clone TIMES OUT in a scheduled run (Partner watch was blocked four runs in a row, Nov 19-22).
Do this instead; it takes about 20 seconds:

```
git config remote.origin.promisor true
git config remote.origin.partialclonefilter blob:none
git fetch -q --depth 1 --filter=blob:none origin partner-catalogs-sqsp
git sparse-checkout set --no-cone '/*' '!/assets/' '!/site-app/'
git checkout -q -B partner-catalogs-sqsp FETCH_HEAD
```

Starting from nothing: `git clone -q --depth 1 --filter=blob:none --sparse --branch partner-catalogs-sqsp <repo url> repo`,
then `cd repo && git sparse-checkout set --no-cone '/*' '!/assets/' '!/site-app/'`.

Then read `CLAUDE.md` on that branch before doing anything else.

- `assets/` and `site-app/` are left out because they are the heavy part. Need a folder from them? `git sparse-checkout add assets/launches/<folder>` (each file is downloaded on demand).
- Adding a NEW file under `assets/` or `site-app/`: write it, then `git add --sparse <path>`.
- Push as usual: `git pull -q --rebase --autostash origin partner-catalogs-sqsp && git push -q origin HEAD:partner-catalogs-sqsp`. If the pull itself is slow, `git fetch -q --depth 1 --filter=blob:none origin partner-catalogs-sqsp && git rebase FETCH_HEAD`.
- Never report "repo could not be cloned" without trying the recipe above first.
