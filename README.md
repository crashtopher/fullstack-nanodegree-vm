To Run This Program:
1. open Terminal and cd to .../fullstack/vagrant/tournament
2. run command vagrant ssh
3. import the database:
    - run cd /vagrant/tournament
    - run command psql
    - run command \i tournament.sql
    - run command \q
4. test program by running python tournament_test.py