from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

# Simulate KDC: Key Distribution Center
# (Authentication Server and Ticket Granting Server combined)
class KDC:
    def __init__(self, client_key, service_key):
        self.client_key = client_key
        self.service_key = service_key
        self.tgt_lifetime = 600

    # Simulate AS: Issue Ticket-Granting Ticket (TGT)
    def issue_tgt(self, client_name):
        tgt_data = f"TGT:{client_name}:{self.tgt_lifetime}".encode('utf-8')
        print(f"KDC: Issuing TGT for client. Raw: {tgt_data}")
        return self._encrypt(tgt_data, self.client_key)

    # Simulate TGS: Issue Service Ticket (based on TGT)
    def issue_service_ticket(self, tgt, client_name, service_name):
        decrypted_tgt = self._decrypt(tgt, self.client_key)
        print(f"KDC: Verifying TGT and issuing Service Ticket. Raw: {decrypted_tgt}")
        if f"TGT:{client_name}" in decrypted_tgt.decode('utf-8'):
            service_ticket_data = f"ST:{client_name}:{service_name}".encode('utf-8')
            print(f"KDC: Issuing Service Ticket. Raw: {service_ticket_data}")
            return self._encrypt(service_ticket_data, self.service_key)
        else:
            raise ValueError("Invalid TGT")
        
    def _encrypt(self, data, key):
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        return base64.b64encode(cipher.nonce + tag + ciphertext).decode('utf-8')
    
    def _decrypt(self, data, key):
        data = base64.b64decode(data)
        nonce = data[:16]
        tag = data[16:32]
        ciphertext = data[32:]
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag)

# Simulate Client
class Client:
    def __init__(self, client_name, kdc, client_key):
        self.client_name = client_name
        self.kdc = kdc
        self.client_key = client_key
        self.tgt = None

    # Step 1: Request TGT from KDC
    def request_tgt(self):
        print(f"Client: Requesting TGT from KDC for {self.client_name}")
        self.tgt = self.kdc.issue_tgt(self.client_name)
        print(f"Client: Received encrypted TGT: {self.tgt}")

    # Step 2: Request Service Ticket from TGS
    def request_service_ticket(self, service_name):
        if not self.tgt:
            raise ValueError("No TGT available. Request TGT first.")
        service_ticket = self.kdc.issue_service_ticket(self.tgt, self.client_name, service_name)
        print(f"Client: Requesting Service Ticket from TGS for {service_name}. Encrypted: {service_ticket}")
        return service_ticket

# Simulate Service
class Service:
    def __init__(self, service_name, service_key):
        self.service_name = service_name
        self.service_key = service_key

    # Step 3: Verify Service Ticket from Client and grant access
    def verify_service_ticket(self, service_ticket):
        decrypted_ticket = self._decrypt(service_ticket, self.service_key)
        print(f"Service: Verifying Service Ticket. Raw: {decrypted_ticket}")
        if f"ST:" in decrypted_ticket.decode('utf-8'):
            print(f"Service: Access granted to {self.service_name}")
        else:
            raise ValueError("Invalid Service Ticket")
    
    # Intensionally not using the KDC's _decrypt method to show that the service can decrypt the ticket
    def _decrypt(self, data, key):
        data = base64.b64decode(data)
        nonce = data[:16]
        tag = data[16:32]
        ciphertext = data[32:]
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag)


def simulate_kerberos_flow():
    # Shared keys for encryption (in reality, these would be securely generated and stored)
    client_key = get_random_bytes(16)
    service_key = get_random_bytes(16)

    # Initialize KDC, Client and Service
    kdc = KDC(client_key, service_key)
    client = Client("Alice", kdc, client_key)
    service = Service("FileServer", service_key)

    # Client requests a TGT from KDC
    client.request_tgt()

    # Client requests a Service Ticket using the TGT
    service_ticket = client.request_service_ticket("FileServer")

    # Service verifies the Service Ticket and grants access
    service.verify_service_ticket(service_ticket)
    

# Run the simulation
simulate_kerberos_flow()