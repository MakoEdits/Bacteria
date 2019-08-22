import names, random, string

class User:
    def __init__(self, **kwargs):
        maxLevel = 100
        # If kwarg is passed, use it, else generate
        self.firstName = kwargs["firstName"] if kwargs["firstName"] != "" else self.genFirstName()
        self.lastName = kwargs["lastName"] if kwargs["lastName"] != "" else self.genLastName()
        self.email = kwargs["email"] if kwargs["email"] != "" else self.genEmail()
        self.password = kwargs["password"] if kwargs["password"] != "" else self.genPassword()
        self.level = kwargs["level"] if kwargs["level"] >= 1 else int(random.randint(1, maxLevel))

    # Applies random case to random variation of input
    def randomCase(self, wordList):
        word = random.choice(wordList)
        if word.isnumeric():
            cased = word
        else:
            cased = random.choice([ word.upper(), word.lower(), word.title(), word ])
        return cased

    # Get random name from names library
    def genFirstName(self):
        firstName = names.get_first_name()
        return firstName

    # Get random name from names library
    def genLastName(self):
        lastName = names.get_last_name()
        return lastName

    # Generate sections of email randomly based on inputs
    def genEmail(self):
        emailPart1 = self.randomCase([
            self.firstName,
            self.firstName[0],
            self.firstName[:int(random.randint(0, len(self.firstName)))]
        ])

        emailPart2 = self.randomCase([
            self.firstName,
            self.firstName[:int(random.randint(0, len(self.firstName)))],
            self.lastName,
            self.lastName[:int(random.randint(0, len(self.lastName)))],
            str(random.randint(0, 100))
        ])

        emailPart3 = self.randomCase([
            str(random.randint(0, 100)), ""
        ])

        # Generate domain based on list of 25 most popular domains
        emailPart4 = "@" + random.choice(open("src/email_set.txt", "r").readlines()).strip("\n")

        email = "".join([emailPart1, emailPart2, emailPart3, emailPart4])
        return email

    # Generate random password by randomly choosing 8 to 16 characters
    def genPassword(self):
        password = "".join(random.choice(
            string.ascii_letters + string.punctuation + string.digits
        ) for x in range(random.randint(8, 12)))
        return password
