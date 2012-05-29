DIRECTORY_HEADER = '''
<CiscoIPPhoneDirectory>

  <Title>%(title)s</Title>

  <Prompt>%(prompt)s</Prompt>
'''

DIRECTORY_FOOTER = '''
</CiscoIPPhoneDirectory>
'''

DIRECTORY_ENTRY = '''
  <DirectoryEntry>
    <Name>%(name)s</Name>
    <Telephone>%(telephone)s</Telephone>
  </DirectoryEntry>
'''

SOFTKEY_ITEM = '''
<SoftKeyItem>
<Name>%(name)s</Name>
<URL>%(url)s</URL>
<Position>%(position)d</Position>
</SoftKeyItem>
'''

MENU_HEADER = '''
<CiscoIPPhoneMenu>

  <Title>%(title)s</Title>

  <Prompt>%(prompt)s</Prompt>
'''

MENU_ITEM = '''
  <MenuItem>
   <Name>%(name)s</Name>
   <URL>%(url)s</URL>
  </MenuItem>
'''

MENU_FOOTER = '''
</CiscoIPPhoneMenu>
'''

PHONE_STATUS = '''
<CiscoIPPhoneStatus>
<Text>%(text)s</Text>
</CiscoIPPhoneStatus> 
'''
