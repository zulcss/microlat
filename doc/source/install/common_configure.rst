2. Edit the ``/etc/microlat/microlat.conf`` file and complete the following
   actions:

   * In the ``[database]`` section, configure database access:

     .. code-block:: ini

        [database]
        ...
        connection = mysql+pymysql://microlat:MICROLAT_DBPASS@controller/microlat
