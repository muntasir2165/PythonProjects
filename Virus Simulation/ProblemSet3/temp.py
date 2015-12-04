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
