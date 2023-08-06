# {{{ project.name }}}
# {{{ author.name }}}

PROJECT={{{ project.name }}}

presentation:
	cd presentation && Rscript -e "library(rmarkdown); rmarkdown::render('$(PROJECT).Rmd')"
	cp presentation/$(PROJECT).html docs/index.html
	cp -r presentation/$(PROJECT)_files docs
	cp -r presentation/assets docs

open:
	open docs/index.html

clean:
	rm -rf docs
	mkdir docs
	rm -f presentation/$(PROJECT).md
	rm -f presentation/$(PROJECT).pdf
	rm -f presentation/$(PROJECT).html
	rm -rf presentation/$(PROJECT)_files
	rm -rf presentation/_bookdown_files
	rm -rf presentation/_book

release: clean presentation
	git commit -am "release"
	git push

serve:
	cd docs && python -m SimpleHTTPServer

.PHONY: presentation release open clean serve
