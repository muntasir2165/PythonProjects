# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics

import numpy
import random
import pylab

'''
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 2
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.
        maxBirthProb: Maximum reproduction probability (a float between 0-1)
        clearProb: Maximum clearance probability (a float between 0-1).
        """

        # TODO
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        # TODO
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        # TODO
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step.
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """

        # TODO
        if random.random() < self.getClearProb():
            return True
        else:
            return False

       #alternate implementation
       #return  random.random() < self.getClearProb()

    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.

        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """

        # TODO
        if self.getMaxBirthProb() * (1 - popDensity) > random.random():
            return SimpleVirus(self.getMaxBirthProb(), self.getClearProb())
        else:
            raise NoChildException()


class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """

        # TODO
        self.viruses = viruses
        self.maxPop = maxPop

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        # TODO
        return self.viruses

    def getMaxPop(self):
        """
        Returns the max population.
        """
        # TODO
        return self.maxPop

    def getTotalPop(self):
        """
        Gets the size of the current total virus population.
        returns: The total virus population (an integer)
        """

        # TODO
        return len(self.getViruses())

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:

        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.

        - The current population density is calculated. This population density
          value is used until the next call to update()

        - Based on this value of population density, determine whether each
          virus particle should reproduce and add offspring virus particles to
          the list of viruses in this patient.

        returns: The total virus population at the end of the update (an
        integer)
        """

        # TODO
        #determine the list of survivor viruses
        survivor_viruses = []
        for virus in self.getViruses():
            if not virus.doesClear():
                survivor_viruses.append(virus)

        #update the virus particles list
        self.viruses = survivor_viruses

        #determine the virus population density
        popDensity = (self.getTotalPop()*1.0)/self.getMaxPop()

        offspring_viruses = []
        for virus in self.getViruses():
            try:
                offspring = virus.reproduce(popDensity)
                offspring_viruses.append(offspring)
            except NoChildException:
                pass

        #update the virus particles list
        self.viruses = self.viruses + offspring_viruses

        return self.getTotalPop()


#
# PROBLEM 3
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """

    # TODO
    #run the simulation
    virus_population_per_trial = []
    virus_population = []
    time_steps = 300

    for trial in range(numTrials):
        #create a list of  numViruses viruses
        viruses = []
        for current in range(numViruses):
    	    virus = SimpleVirus(maxBirthProb, clearProb)
            viruses.append(virus)

        #instatiate a patient with viruses and maxPop
        patient = Patient(viruses, maxPop)
        total_viruses = []

        for time_step in range(time_steps):
            total_viruses.append(patient.update())

    virus_population_per_trial.append(total_viruses)

    #find the average total number of viruses for each time step
    for index in range(time_steps):
        total_virus_numbers = 0.0
        for total_list in virus_population_per_trial:
            total_virus_numbers += total_list[index]
        virus_population.append(total_virus_numbers/numTrials)

    #plot the results
    #print "x: ", len(range(time_steps)) #=>300
    #print "y: ", len(virus_population)    #=>300
    pylab.plot(range(time_steps), virus_population, label='Virus without drug resistance')
    pylab.xlabel('Number of Elapsed Time Steps')
    pylab.ylabel('Average Size of the Virus Population')
    pylab.title('Changes in the Virus Population in a Patient over 300 Time Steps')
    pylab.legend()
    pylab.show()

'''
#Alternate working implementation
#Please note that although this alternate solution works, I am not sure why
#since to me this solution is obviously flawed
#
# PROBLEM 3
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """

    # TODO
    #run the simulation
    virus_population = []
    time_steps = 300
    for time_step in range(time_steps):
        #create a list of  numViruses viruses
        viruses = []
        for current in range(numViruses):
    	    virus = SimpleVirus(maxBirthProb, clearProb)
            viruses.append(virus)

        #instatiate a patient with viruses and maxPop
        patient = Patient(viruses, maxPop)
        total_viruses = 0
        for trial in range(numTrials):
            total_viruses += patient.update()
        average_total_viruses = int((1.0 * total_viruses) / numTrials)
        numViruses = average_total_viruses
        virus_population.append(float(average_total_viruses))

    #plot the results
    #print "x: ", len(range(time_steps)) #=>300
    #print "y: ", len(virus_population)    #=>300
    pylab.plot(range(time_steps), virus_population, label='Virus without drug resistance')
    pylab.xlabel('Number of Elapsed Time Steps')
    pylab.ylabel('Average Size of the Virus Population')
    pylab.title('Changes in the Virus Population in a Patient over 300 Time Steps')
    pylab.legend()
    pylab.show()
'''

#optional
#from ps3b_precompiled_27 import *

#function test call
#simulationWithoutDrug(100, 1000, 0.1, 0.05, 100)


#
# PROBLEM 4
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """

        # TODO
        #self.maxBirthProb = maxBirthProb
        #self.clearProb = clearProb
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb

    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        # TODO
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        # TODO
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """

        # TODO
        return self.getResistances().get(drug, False)

    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:

        self.maxBirthProb * (1 - popDensity).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """

        # TODO
        #check if the virus is resistant to all drugs in activeDrugs
        for drug in activeDrugs:
            if not self.isResistantTo(drug):
                raise NoChildException

        #if the virus is resistant to all drugs in activeDrugs, then the
        #virus reproduces with probability...
        do_reproduce = False
        if  self.maxBirthProb * (1 - popDensity) > random.random():
            do_reproduce = True

        if not do_reproduce:
            raise NoChildException
        else:
            offspring_resistances = {}
            for drug in self.getResistances().keys():
                if (1-self.getMutProb()) > random.random():
                    offspring_resistances[drug] = self.isResistantTo(drug)
                else:
                    offspring_resistances[drug] = not self.isResistantTo(drug)
            return ResistantVirus(self.getMaxBirthProb(), self.getClearProb(), offspring_resistances, self.getMutProb())

class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """

        # TODO
        Patient.__init__(self, viruses, maxPop)
        self.drugs_list = []

    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """

        # TODO
        if newDrug not in self.drugs_list:
            self.drugs_list.append(newDrug)

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """

        # TODO
        return self.drugs_list

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """

        # TODO
        resistant_population = []
        for virus in self.getViruses():
            resistant_to_all = 0
            for drug in drugResist:
                if virus.isResistantTo(drug):
                    resistant_to_all += 1
            if resistant_to_all == len(drugResist):
                resistant_population.append(virus)
        return len(resistant_population)

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each
          virus particle should reproduce and add offspring virus particles to
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """

        # TODO
        #determine the list of survivor viruses
        survivor_viruses = []
        for virus in self.getViruses():
            if not virus.doesClear():
                survivor_viruses.append(virus)

        #update the virus particles list
        self.viruses = survivor_viruses

        #determine the virus population density
        popDensity = (self.getTotalPop()*1.0)/self.getMaxPop()

        #determine the list of offstring viruses
        offspring_viruses = []
        for virus in self.getViruses():
            try:
                offspring = virus.reproduce(popDensity, self.getPrescriptions())
                offspring_viruses.append(offspring)
            except NoChildException:
                pass

        #update the virus particles list
        self.viruses = self.viruses + offspring_viruses

        return self.getTotalPop()


#
# PROBLEM 5
#
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1).
    numTrials: number of simulation runs to execute (an integer)

    """

    # TODO
    #run the simulation
    virus_population_per_trial = []
    virus_population = []
    guttagonol_resistant_population_per_trial = []
    guttagonol_resistant_population = []
    time_steps = 300

    for trial in range(numTrials):
        #create a list of  numViruses viruses
        viruses = []
        for current in range(numViruses):
    	    virus = ResistantVirus(maxBirthProb, clearProb, resistances, mutProb)
            viruses.append(virus)

        #instatiate a patient with viruses and maxPop
        patient = TreatedPatient(viruses, maxPop)

        #counter variable for the total number of viruses and
        #guttagonol resistant viruses inside the patient for time_steps
        #number of time steps
        total_viruses = []
        guttagonol_resistant_viruses = []

        for time_step in range(time_steps):
            #add guttagonol drug to the patient's prescription
            #for the final 150 time steps
            if time_step >= 150:
                patient.addPrescription('guttagonol')
            total_viruses.append(patient.update())

            #determine the number of guttagonol resistant viruses
            guttagonol_resistant_viruses_number = 0
            for virus in patient.getViruses():
                if virus.isResistantTo('guttagonol'):
                    guttagonol_resistant_viruses_number += 1
            guttagonol_resistant_viruses.append(guttagonol_resistant_viruses_number)

        virus_population_per_trial.append(total_viruses)
        guttagonol_resistant_population_per_trial.append(guttagonol_resistant_viruses)

    #find the average total number of viruses and guttagonol resistant viruses for each
    #time step
    for index in range(time_steps):
        total_virus = 0.0
        total_guttagonol_resistant = 0.0
        for total_list, guttagonol_list in zip(virus_population_per_trial, guttagonol_resistant_population_per_trial):
            total_virus += total_list[index]
            total_guttagonol_resistant += guttagonol_list[index]
        virus_population.append(total_virus/numTrials)
        guttagonol_resistant_population.append(total_guttagonol_resistant/numTrials)

    #plot the results
    pylab.plot(range(time_steps), virus_population, label='Average total virus population')
    pylab.plot(range(time_steps), guttagonol_resistant_population, label='Average population of guttagonol-resistant virus particles')
    pylab.xlabel('Elapsed Time Steps')
    pylab.ylabel('Average Size of the Virus Population')
    pylab.title('Changes in the Virus Population in a Patient over 300 Time Steps')
    pylab.legend()
    pylab.show()

#optional
#from ps3b_precompiled_27 import *

#function test call
#simulationWithDrug(100, 1000, 0.1, 0.05,  {'guttagonol': False}, 0.005, 100)
