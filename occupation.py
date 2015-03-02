from event import *


class Occupation(object):
    """An occupation at a business in a city."""

    def __init__(self, person, company, shift):
        """Initialize an Occupation object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        @param shift: Whether this position is for the day or night shift.
        """
        self.person = person
        self.company = company
        self.shift = shift
        self.company.employees.add(self)
        self.start_date = person.game.year
        self.hiring = None  # event.Hiring object holding data about the hiring; gets set by that object's __init__()
        self.end_date = None  # Changed by self.terminate
        self.terminus = None  # Changed by self.terminate
        # Note: self.person.occupation gets set by Business.hire(), because there's
        # a really tricky pipeline that has to be maintained
        self.person.occupations.append(self)
        # Set job level of this occupation
        self.level = person.game.config.job_levels[self.__class__]
        # Set industry and what industry a potential applicant must come from to be hired for this occupation
        self.industry = person.game.config.industries[self.__class__]
        self.prerequisite_industry = person.game.config.prerequisite_industries[self.__class__]

    def __str__(self):
        """Return string representation."""
        return "{0} at {1}".format(self.__class__.__name__, self.company.name)

    @property
    def years_experience(self):
        """Return years this person has had this occupation."""
        return self.person.game.year - self.start_date

    def terminate(self, reason):
        """Terminate this occupation, due to another hiring, retirement, or death or departure."""
        self.end_date = self.person.game.year
        self.terminus = reason
        if not isinstance(reason, Hiring) and reason.promotion:
            self.company.employees.remove(self)
            self.company.former_employees.add(self)
        # If the person hasn't already been hired to a new position, set their
        # occupation attribute to None
        if self.person.occupation is self:
            self.person.occupation = None
        # This position is now vacant, so now have the company that this person worked
        # for fill that now vacant position (which may cause a hiring chain)
        position_that_is_now_vacant = self.__class__
        self.company.hire(occupation_of_need=position_that_is_now_vacant)


##################################
##      BUSINESS-INDEPENDENT    ##
##################################


class Cashier(Occupation):
    """A cashier at a business."""

    def __init__(self, person, company, shift):
        """Initialize a Cashier object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        """
        super(Cashier, self).__init__(person=person, company=company, shift=shift)


class Janitor(Occupation):
    """A janitor at a business."""

    def __init__(self, person, company, shift):
        """Initialize a Janitor object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        """
        super(Janitor, self).__init__(person=person, company=company, shift=shift)


class Manager(Occupation):
    """A manager at a business."""

    def __init__(self, person, company, shift):
        """Initialize an Owner object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        """
        super(Manager, self).__init__(person=person, company=company, shift=shift)


class Secretary(Occupation):
    """A secretary at a business."""

    def __init__(self, person, company, shift):
        """Initialize an Secretary object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        """
        super(Secretary, self).__init__(person=person, company=company, shift=shift)


class Owner(Occupation):
    """An owner of a business."""

    def __init__(self, person, company, shift):
        """Initialize an Owner object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        """
        super(Owner, self).__init__(person=person, company=company, shift=shift)


##################################
##      BUSINESS-SEMIDEPENDENT  ##
##################################


class Groundskeeper(Occupation):
    """A mortician at a cemetery or park."""

    def __init__(self, person, company, shift):
        """Initialize a Mortician object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        """
        super(Groundskeeper, self).__init__(person=person, company=company, shift=shift)


class Nurse(Occupation):
    """A nurse at a hospital, optometry clinic, plastic-surgery clinic, or school."""

    def __init__(self, person, company, shift):
        """Initialize a Nurse object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        """
        super(Nurse, self).__init__(person=person, company=company, shift=shift)


##################################
##      BUSINESS-DEPENDENT      ##
##################################


class Architect(Occupation):
    """An architect at a construction firm."""

    def __init__(self, person, company, shift):
        """Initialize an Architect object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        """
        super(Architect, self).__init__(person=person, company=company, shift=shift)
        # Work accomplishments
        self.building_constructions = set()
        self.house_constructions = set()

    def construct_building(self, client, business):
        """Return a constructed building."""
        construction = BusinessConstruction(subject=client, business=business, architect=self)
        return construction

    def construct_house(self, clients, lot):
        """Return a constructed building."""
        construction = HouseConstruction(subjects=clients, architect=self, lot=lot)
        return construction.house


class BankTeller(Occupation):
    """A bank teller at a bank."""

    def __init__(self, person, company, shift):
        """Initialize a BankTeller object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        """
        super(BankTeller, self).__init__(person=person, company=company, shift=shift)


class Bartender(Occupation):
    """A bartender at a bar."""

    def __init__(self, person, company, shift):
        """Initialize a Bartender object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        """
        super(Bartender, self).__init__(person=person, company=company, shift=shift)


class BusDriver(Occupation):
    """A bus driver at a bus depot."""

    def __init__(self, person, company, shift):
        """Initialize a BusDriver object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        """
        super(BusDriver, self).__init__(person=person, company=company, shift=shift)


class Concierge(Occupation):
    """A concierge at a hotel."""

    def __init__(self, person, company, shift):
        """Initialize a Concierge object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        """
        super(Concierge, self).__init__(person=person, company=company, shift=shift)


class ConstructionWorker(Occupation):
    """A construction worker at a construction firm."""

    def __init__(self, person, company, shift):
        """Initialize a ConstructionWorker object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        """
        super(ConstructionWorker, self).__init__(person=person, company=company, shift=shift)


class DayCareProvider(Occupation):
    """A person who works at a day care."""

    def __init__(self, person, company, shift):
        """Initialize a DayCareProvider object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        """
        super(DayCareProvider, self).__init__(person=person, company=company, shift=shift)


class Doctor(Occupation):
    """A doctor at a hospital."""

    def __init__(self, person, company, shift):
        """Initialize a Doctor object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        """
        super(Doctor, self).__init__(person=person, company=company, shift=shift)
        # Work accomplishments
        self.baby_deliveries = set()

    def deliver_baby(self, mother):
        """Instantiate a new Birth object."""
        Birth(mother=mother, doctor=self)


class FireChief(Occupation):
    """A fire chief at a fire station."""

    def __init__(self, person, company, shift):
        """Initialize a FireChief object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        """
        super(FireChief, self).__init__(person=person, company=company, shift=shift)


class Firefighter(Occupation):
    """A firefighter at a fire station."""

    def __init__(self, person, company, shift):
        """Initialize a Firefighter object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        """
        super(Firefighter, self).__init__(person=person, company=company, shift=shift)


class HairStylist(Occupation):
    """A hair stylist at a barbershop."""

    def __init__(self, person, company, shift):
        """Initialize a HairStylist object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        """
        super(HairStylist, self).__init__(person=person, company=company, shift=shift)


class HotelMaid(Occupation):
    """A hotel maid at a hotel."""

    def __init__(self, person, company, shift):
        """Initialize a HotelMaid object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        """
        super(HotelMaid, self).__init__(person=person, company=company, shift=shift)


class Lawyer(Occupation):
    """A lawyer at a law firm."""

    def __init__(self, person, company, shift):
        """Initialize a Lawyer object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        """
        super(Lawyer, self).__init__(person=person, company=company, shift=shift)
        # Work accomplishments
        self.filed_divorces = set()
        self.filed_name_changes = set()

    def file_divorce(self, clients):
        """File a name change on behalf of person."""
        Divorce(subjects=clients, lawyer=self)

    def file_name_change(self, person, new_last_name, reason):
        """File a name change on behalf of person."""
        NameChange(subject=person, new_last_name=new_last_name, reason=reason, lawyer=self)


class Mayor(Occupation):
    """A mayor at the city hall."""

    def __init__(self, person, company, shift):
        """Initialize a Mayor object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        """
        super(Mayor, self).__init__(person=person, company=company, shift=shift)


class Mortician(Occupation):
    """A mortician at a cemetery."""

    def __init__(self, person, company, shift):
        """Initialize a Mortician object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        """
        super(Mortician, self).__init__(person=person, company=company, shift=shift)
        # Work accomplishments
        self.body_interments = set()

    def inter_body(self, deceased, cause_of_death):
        """Inter a body in a cemetery."""
        Death(subject=deceased, mortician=self, cause_of_death=cause_of_death)


class Optometrist(Occupation):
    """An optometrist at an optometry clinic."""

    def __init__(self, person, company, shift):
        """Initialize an Optometrist object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        """
        super(Optometrist, self).__init__(person=person, company=company, shift=shift)


class PlasticSurgeon(Occupation):
    """A plastic surgeon at a plastic-surgery clinic."""

    def __init__(self, person, company, shift):
        """Initialize a PlasticSurgeon object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        """
        super(PlasticSurgeon, self).__init__(person=person, company=company, shift=shift)


class PoliceChief(Occupation):
    """A police chief at a police station."""

    def __init__(self, person, company, shift):
        """Initialize a PoliceChief object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        """
        super(PoliceChief, self).__init__(person=person, company=company, shift=shift)


class PoliceOfficer(Occupation):
    """A police officer at a police station."""

    def __init__(self, person, company, shift):
        """Initialize a PoliceOfficer object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        """
        super(PoliceOfficer, self).__init__(person=person, company=company, shift=shift)


class Realtor(Occupation):
    """A realtor at a realty firm."""

    def __init__(self, person, company, shift):
        """Initialize an Realtor object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        """
        super(Realtor, self).__init__(person=person, company=company, shift=shift)
        # Work accomplishments
        self.home_sales = set()

    def sell_home(self, clients, home):
        """Return a sold home."""
        home_sales = HomePurchase(subjects=clients, home=home, realtor=self)
        return home_sales.home


class Professor(Occupation):
    """A professor at the university."""

    def __init__(self, person, company, shift):
        """Initialize a Professor object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        """
        super(Professor, self).__init__(person=person, company=company, shift=shift)


class TattooArtist(Occupation):
    """A tattoo artist at a tattoo parlor."""

    def __init__(self, person, company, shift):
        """Initialize a TattooArtist object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        """
        super(TattooArtist, self).__init__(person=person, company=company, shift=shift)


class TaxiDriver(Occupation):
    """A taxi driver at a taxi depot."""

    def __init__(self, person, company, shift):
        """Initialize a TaxiDriver object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        """
        super(TaxiDriver, self).__init__(person=person, company=company, shift=shift)


class Teacher(Occupation):
    """A teacher at the K-12 school."""

    def __init__(self, person, company, shift):
        """Initialize a Teacher object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        """
        super(Teacher, self).__init__(person=person, company=company, shift=shift)


class Waiter(Occupation):
    """A waiter at a restaurant."""

    def __init__(self, person, company, shift):
        """Initialize a Waiter object.

        @param person: The Person object for the person whose occupation this is.
        @param company: The Company object for the company that person works for in this capacity.
        """
        super(Waiter, self).__init__(person=person, company=company, shift=shift)
