To Run This Program:
1. In terminal cd ~/path/to/this/file
2. run vagrant up
3. run vagrant ssh
4. import the database:
    - run cd /vagrant/tournament
    - run command psql
    - run command \i tournament.sql
    - run command \q
5. test program by running python tournament_test.py