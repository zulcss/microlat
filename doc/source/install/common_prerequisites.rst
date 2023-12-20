Prerequisites
-------------

Before you install and configure the microlat service,
you must create a database, service credentials, and API endpoints.

#. To create the database, complete these steps:

   * Use the database access client to connect to the database
     server as the ``root`` user:

     .. code-block:: console

        $ mysql -u root -p

   * Create the ``microlat`` database:

     .. code-block:: none

        CREATE DATABASE microlat;

   * Grant proper access to the ``microlat`` database:

     .. code-block:: none

        GRANT ALL PRIVILEGES ON microlat.* TO 'microlat'@'localhost' \
          IDENTIFIED BY 'MICROLAT_DBPASS';
        GRANT ALL PRIVILEGES ON microlat.* TO 'microlat'@'%' \
          IDENTIFIED BY 'MICROLAT_DBPASS';

     Replace ``MICROLAT_DBPASS`` with a suitable password.

   * Exit the database access client.

     .. code-block:: none

        exit;

#. Source the ``admin`` credentials to gain access to
   admin-only CLI commands:

   .. code-block:: console

      $ . admin-openrc

#. To create the service credentials, complete these steps:

   * Create the ``microlat`` user:

     .. code-block:: console

        $ openstack user create --domain default --password-prompt microlat

   * Add the ``admin`` role to the ``microlat`` user:

     .. code-block:: console

        $ openstack role add --project service --user microlat admin

   * Create the microlat service entities:

     .. code-block:: console

        $ openstack service create --name microlat --description "microlat" microlat

#. Create the microlat service API endpoints:

   .. code-block:: console

      $ openstack endpoint create --region RegionOne \
        microlat public http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        microlat internal http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        microlat admin http://controller:XXXX/vY/%\(tenant_id\)s
