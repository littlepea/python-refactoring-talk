jupyter-nbconvert --to slides refactoring.ipynb
git commit -a -m "update slides"

git checkout -B gh-pages
mv refactoring.slides.html index.html
git commit -a -m "update pages"
git push origin master gh-pages

git checkout master
git push origin master