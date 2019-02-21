# Collective Conscience

## What it is

- Utilizes IBM's natural language processing and the google custom search API to provide automated 'google search' research and summarizations of topics of interests to clients.

- Interface gives the 'feel' of having a personal research intern (hence the name)

- Python/ Flask,  MySQL backend. Frontend React-Redux. Fullstack application
## Projectes current state

- The IBM natural langunage processing portion is not implemented. The analysis part  was implemented before as a R script, but due to integration issues it was removed from the project. That part needs to be completely reimplemented

- Currently no interface. There is no UI. I would like this to be built in react

- Currently it is a command line application. The command line application can automate google research and create accounts and persist data locally

- There is no dev or prod environment or ci/cd workflow

- There is no unit tests

- The project is not possible to iterate on without writing unit tests and slowly rebuilding the banckend into an API and placing the google search logic in the frontend

## Next steps

- To containerize the application via docker and build a nice CI/CD workflow as I build the backend into an API (with unit tests) and move the search logic into the frontend

- To place open source licensing and to document it more so it is easier for others to work on

- To fix the file structure so it is more intuitive
