SCADE Lab Portfolio
Local development setup for the docs site (Jekyll)

============================================================
Prerequisites
============================================================
1. Install Ruby (all options)

============================================================
First-time setup
============================================================
cd docs
bundle install

============================================================
Run local server
============================================================
cd docs
bundle exec jekyll serve

-> Open http://localhost:4000/ in your browser
-> The site reloads automatically when you edit markdown/html files
-> Press Ctrl+C to stop the server

============================================================
Notes
============================================================
- Portfolio page  : docs/index.html
- Lab pages       : docs/lab2/, docs/lab3_1/, docs/lab3_2/ (each has index.html + lab.md)
- Lab source code : src/lab2/, src/lab3_1/, src/lab3_2/ (starter/solution files)

After updating Gemfile, run: bundle install
