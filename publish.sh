git commit -a -m "update slides"

git checkout -B gh-pages
jupyter-nbconvert --to slides refactoring.ipynb
mv refactoring.slides.html index.html
git commit -a -m "update pages"
git push origin master gh-pages

git checkout master
rm -rf index.html
git push origin master