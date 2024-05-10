import random
from faker import Faker


class Voter:
    def __init__(self, first_name, last_name, age, voter_id):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.voter_id = voter_id
        self.voted = False

class List:
    def __init__(self, name):
        self.name = name
        self.candidates = []

    def add_candidate(self, candidate):
        self.candidates.append(candidate)

class Ballot:
    def __init__(self, voter_id, choices):
        self.voter_id = voter_id
        self.choices = choices

class BallotBox:
    def __init__(self):
        self.ballots = []

    def deposit_ballot(self, ballot):
        self.ballots.append(ballot)

class Scanner:
    def scan_ballot(self, ballot):
        # Simulate scanning process
        return True  # Assume all scanned ballots are valid

class VotingMachine:
    def __init__(self, usb_stick):
        self.usb_stick = usb_stick
        self.ballot_box = BallotBox()
        self.scanner = Scanner()
        self.fake = Faker()

    def process_vote(self, voter, choices):
        if not voter.voted:
            ballot = Ballot(voter.voter_id, choices)
            self.ballot_box.deposit_ballot(ballot)
            voter.voted = True
            return self.scanner.scan_ballot(ballot)
        else:
            raise ValueError("Voter has already voted.")

class ChipCard:
    def __init__(self, initialized=False):
        self.initialized = initialized

class USBStick:
    def __init__(self, code):
        self.code = code

class VotingSystem:
    def __init__(self):
        self.voters = []
        self.lists = []
        self.voting_machines = []
        self.usb_stick = USBStick(code='START123')
        self.chip_cards = [ChipCard() for _ in range(60)]

    def setup(self):
        # Initializing voters
        for _ in range(1200):
            first_name = self.fake.first_name()
            last_name = self.fake.last_name()
            age = random.randint(18, 90)
            voter_id = self.fake.uuid4()
            self.voters.append(Voter(first_name, last_name, age, voter_id))

        # Creating lists and assigning candidates
        list_names = ['List A', 'List B', 'List C', 'List D', 'List E']
        for name in list_names:
            party_list = List(name)
            candidates = random.sample(self.voters, 10)
            for candidate in candidates:
                party_list.add_candidate(candidate)
            self.lists.append(party_list)

        # Initializing voting machines
        for _ in range(3):
            machine = VotingMachine(self.usb_stick)
            self.voting_machines.append(machine)

    def simulate_voting_process(self):
        # Randomly simulate voting process
        for voter in self.voters:
            if not voter.voted:
                chosen_list = random.choice(self.lists)
                if random.choice([True, False]):  # Randomly deciding between list vote or preference vote
                    choices = [chosen_list.name]
                else:
                    choices = [random.choice(chosen_list.candidates).voter_id for _ in range(random.randint(1, 3))]

                machine = random.choice(self.voting_machines)
                try:
                    machine.process_vote(voter, choices)
                except ValueError as e:
                    print(e)

    def generate_html_output(self):
        html_content = '<html><head><title>Election Results</title></head><body>'
        html_content += '<h1>Election Results</h1>'
        for machine in self.voting_machines:
            html_content += f'<h2>Machine {machine.usb_stick.code}</h2><ul>'
            for ballot in machine.ballot_box.ballots:
                html_content += f'<li>Voter ID: {ballot.voter_id}, Votes: {ballot.choices}</li>'
            html_content += '</ul>'
        html_content += '</body></html>'
        return html_content

# Initializing the system and simulating the voting process
voting_system = VotingSystem()
voting_system.setup()
voting_system.simulate_voting_process()
html_output = voting_system.generate_html_output()

# Uncomment below lines to save HTML output to a file and to view it
with open('/mnt/data/Election_Results.html', 'w') as file:
     file.write(html_output)
