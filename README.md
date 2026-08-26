# mihainadas.github.io

Research and engineering notes published at [mihainadas.github.io](https://mihainadas.github.io/).

## Local checks

```sh
bundle install
python3 scripts/check_site.py
bundle exec jekyll build --strict_front_matter
python3 scripts/check_build.py
bundle exec htmlproofer ./_site --disable-external --enforce-https
```

The site uses the GitHub Pages dependency set and the bundled Minima release rather than an unpinned theme branch.
