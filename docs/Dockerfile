FROM jekyll/jekyll:latest
COPY Gemfile /srv/jekyll
RUN bundle install
CMD jekyll serve --watch --force_polling --verbose --livereload
