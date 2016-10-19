git commit -a -m "update slides"

git checkout -B gh-pages
jupyter-nbconvert --to slides refactoring.ipynb
mv refactoring.slides.html index.html
git commit -a -m "update pages"
git pull origin master gh-pages && git push origin master gh-pages

git checkout master
rm -rf index.html
git pull origin master && git push origin master