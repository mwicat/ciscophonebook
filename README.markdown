## Usage

``cisco_ldap``

## Screenshots

### Main menu

![Main menu](https://github.com/downloads/mwicat/ciscophonebook/cisco_ldap_menu.jpg)

### Menu showing groups of users to choose from

![Group listing](https://github.com/downloads/mwicat/ciscophonebook/cisco_ldap_groups.jpg)

### Users in the chosen group

![Group users listing](https://github.com/downloads/mwicat/ciscophonebook/cisco_ldap_users.jpg)

### Search panel

![Search panel](https://github.com/downloads/mwicat/ciscophonebook/cisco_ldap3.jpg)

### Search results

![Search results](https://github.com/downloads/mwicat/ciscophonebook/cisco_ldap4.jpg)


## Testing with server-side

Download DEB file from http://directory.apache.org/apacheds/2.0/download/download-linux-deb.html

### Run apache ds server:

``sudo /etc/init.d/apacheds-2.0.0-M7-default start``

``sudo apt-get install ldap-utils``

Import sample LDIF file to server


``ldapadd -f test/test.ldif -x -h 127.0.0.1 -p 10389``

Save configuration in .ldaprc, format: JSON

```
{
        'hostname': "127.0.0.1",
        'port': 10389,
        'people_dn': 'ou=People'
}
```

## Install

``sudo python setup.py install``

Run with sample configuration file

``cisco_ldap -C test/ldaprc``

## Testing

go to url http://localhost:5000/menu

Installation

TFTP template

```
<device>
  <devicePool>
    <callManagerGroup>
      <members>
        <member priority="0">
          <callManager>
            <ports>
              <ethernetPhonePort>2000</ethernetPhonePort>
            </ports>
            <processNodeName>Asterisk IP here</processNodeName>
          </callManager>
        </member>
      </members>
    </callManagerGroup>
  </devicePool>
  <versionStamp>{Jan 01 2002 00:00:00}</versionStamp>
  <loadInformation></loadInformation>
  <userLocale>
    <name>English_United_States</name>
    <langCode>en</langCode>
  </userLocale>
  <networkLocale>United_States</networkLocale>
  <idleTimeout>0</idleTimeout>
  <authenticationURL></authenticationURL>
  <directoryURL>http://127.0.0.1:8000/menu.xml</directoryURL>
  <idleURL></idleURL>
  <informationURL></informationURL>
  <messagesURL></messagesURL>
  <proxyServerURL></proxyServerURL>
  <servicesURL></servicesURL>
</device>
```
