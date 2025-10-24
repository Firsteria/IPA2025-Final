from ncclient import manager
import xmltodict

# Router IP ที่อนุญาต
ROUTER_IPS = ["10.0.15.61", "10.0.15.62", "10.0.15.63", "10.0.15.64", "10.0.15.65"]

USERNAME = "admin"
PASSWORD = "cisco"
NETCONF_PORT = 830  # ปกติ NETCONF ใช้ port 830

def get_manager(ip):
    """สร้าง session NETCONF"""
    return manager.connect(
        host=ip,
        port=NETCONF_PORT,
        username=USERNAME,
        password=PASSWORD,
        hostkey_verify=False
    )

def safe_get(d, keys, default=None):
    """ดึงค่าจาก nested dict แบบปลอดภัย"""
    for key in keys:
        if isinstance(d, dict):
            d = d.get(key, default)
        else:
            return default
    return d

def create(ip):
    netconf_config = f"""
    <config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>Loopback66070119</name>
          <description>loopback for 66070119</description>
          <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
          <enabled>true</enabled>
          <ietf-ip:ipv4 xmlns:ietf-ip="urn:ietf:params:xml:ns:yang:ietf-ip">
            <ietf-ip:address>
              <ietf-ip:ip>172.1.19.1</ietf-ip:ip>
              <ietf-ip:netmask>255.255.255.0</ietf-ip:netmask>
            </ietf-ip:address>
          </ietf-ip:ipv4>
        </interface>
      </interfaces>
    </config>
    """
    try:
        m = get_manager(ip)
        # ตรวจสอบว่ามี Loopback อยู่แล้ว
        existing = m.get(filter=f"""
        <filter>
          <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
              <name>Loopback66070119</name>
            </interface>
          </interfaces-state>
        </filter>
        """)
        existing_dict = xmltodict.parse(existing.xml)
        interface_data = safe_get(existing_dict, ["rpc-reply","data","interfaces-state","interface"])
        if interface_data:
            return "Cannot create: Interface loopback 66070119"

        netconf_reply = m.edit_config(target="running", config=netconf_config)
        xml_data = netconf_reply.xml
        if "<ok/>" in xml_data:
            return "Interface loopback 66070119 is created successfully"
        else:
            return "Error: Cannot create interface loopback 66070119"
    except Exception as e:
        return f"Error! {e}"

def delete(ip):
    netconf_config = f"""
    <config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface operation="delete">
          <name>Loopback66070119</name>
        </interface>
      </interfaces>
    </config>
    """
    try:
        m = get_manager(ip)
        # ตรวจสอบว่ามี Loopback อยู่
        existing = m.get(filter=f"""
        <filter>
          <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
              <name>Loopback66070119</name>
            </interface>
          </interfaces-state>
        </filter>
        """)
        existing_dict = xmltodict.parse(existing.xml)
        interface_data = safe_get(existing_dict, ["rpc-reply","data","interfaces-state","interface"])
        if not interface_data:
            return "Cannot delete: Interface loopback 66070119"

        netconf_reply = m.edit_config(target="running", config=netconf_config)
        xml_data = netconf_reply.xml
        if "<ok/>" in xml_data:
            return "Interface loopback 66070119 is deleted successfully"
        else:
            return "Error: Cannot delete interface loopback 66070119"
    except Exception as e:
        return f"Error! {e}"

def enable(ip):
    netconf_config = f"""
    <config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>Loopback66070119</name>
          <enabled>true</enabled>
        </interface>
      </interfaces>
    </config>
    """
    try:
        m = get_manager(ip)
        existing = m.get(filter=f"""
        <filter>
          <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
              <name>Loopback66070119</name>
            </interface>
          </interfaces-state>
        </filter>
        """)
        existing_dict = xmltodict.parse(existing.xml)
        interface_data = safe_get(existing_dict, ["rpc-reply","data","interfaces-state","interface"])
        if not interface_data:
            return "Cannot enable: Interface loopback 66070119"

        netconf_reply = m.edit_config(target="running", config=netconf_config)
        xml_data = netconf_reply.xml
        if "<ok/>" in xml_data:
            return "Interface loopback 66070119 is enabled successfully"
        else:
            return "Error: Cannot enable interface loopback 66070119"
    except Exception as e:
        return f"Error! {e}"

def disable(ip):
    netconf_config = f"""
    <config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>Loopback66070119</name>
          <enabled>false</enabled>
        </interface>
      </interfaces>
    </config>
    """
    try:
        m = get_manager(ip)
        existing = m.get(filter=f"""
        <filter>
          <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
              <name>Loopback66070119</name>
            </interface>
          </interfaces-state>
        </filter>
        """)
        existing_dict = xmltodict.parse(existing.xml)
        interface_data = safe_get(existing_dict, ["rpc-reply","data","interfaces-state","interface"])
        if not interface_data:
            return "Cannot shutdown: Interface loopback 66070119"

        netconf_reply = m.edit_config(target="running", config=netconf_config)
        xml_data = netconf_reply.xml
        if "<ok/>" in xml_data:
            return "Interface loopback 66070119 is shutdowned successfully"
        else:
            return "Error: Cannot shutdown interface loopback 66070119"
    except Exception as e:
        return f"Error! {e}"

def status(ip):
    try:
        m = get_manager(ip)
        netconf_filter = f"""
        <filter>
          <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
              <name>Loopback66070119</name>
            </interface>
          </interfaces-state>
        </filter>
        """
        netconf_reply = m.get(netconf_filter)
        existing_dict = xmltodict.parse(netconf_reply.xml)
        interface_data = safe_get(existing_dict, ["rpc-reply","data","interfaces-state","interface"])
        if not interface_data:
            return "No Interface loopback 66070119"

        admin_status = interface_data.get("admin-status")
        oper_status = interface_data.get("oper-status")
        if admin_status == 'up' and oper_status == 'up':
            return "Interface loopback 66070119 is enabled"
        elif admin_status == 'down' and oper_status == 'down':
            return "Interface loopback 66070119 is disabled"
        else:
            return "Interface loopback 66070119 has unknown status"
    except Exception as e:
        return f"Error! {e}"
