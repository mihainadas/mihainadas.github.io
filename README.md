# mihainadas.github.io

Research and engineering notes published at [mihainadas.github.io](https://mihainadas.github.io/).

## Local checks

```sh
bundle install
bundle exec jekyll build --strict_front_matter
bundle exec htmlproofer ./_site --disable-external --enforce-https
python3 scripts/check_site.py
```

The site uses the GitHub Pages dependency set and the bundled Minima release rather than an unpinned theme branch.
