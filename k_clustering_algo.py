import numpy as np
import random
import units
import math
import event_generator
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler
from scipy.optimize import curve_fit
import detector
import makePV

from sklearn.datasets.samples_generator import make_blobs

weight = [1./(detector.timing_detector["resolution"]),1./(detector.velo["resolution"])]

#weight = [1,1]
# Define model function to be used to fit to the data above:
def gauss(x, *p):
    A, mu, sigma = p
    return A*np.exp(-(x-mu)**2/(2.*sigma**2))

def cluster_points(X, mu):
    clusters  = {}
    for x in X:
        bestmukey = min([(i[0],
        			math.sqrt((weight[0] * (x-mu[i[0]])[0])**2 + ( weight[1] * (x-mu[i[0]])[1])**2)/math.sqrt(weight[0]**2 + weight[1]**2)
        			) \
                    for i in enumerate(mu)], key=lambda t:t[1])[0]
        try:
            clusters[bestmukey].append(x)
        except KeyError:
            clusters[bestmukey] = [x]
    return clusters

def reevaluate_centers(mu, clusters):
    newmu = []
    keys = sorted(clusters.keys())
    for k in keys:
        newmu.append(np.mean(clusters[k], axis = 0))
    return newmu

def has_converged(mu, oldmu):
    return ( set([tuple(a) for a in mu]) == set([tuple(a) for a in oldmu]) )
    
def find_centers(X, K):
    # Initialize to K random centers
    oldmu = random.sample(X, K)
    mu = random.sample(X, K)
    while not has_converged(mu, oldmu):
    	#print "Iterating clustering algorithm."
        oldmu = mu
        # Assign all points in X to clusters
        clusters = cluster_points(X, mu)
        # Reevaluate centers
        mu = reevaluate_centers(oldmu, clusters)
    return(mu, clusters)
    
def generate_pull_histogram( offsets ):
	"""
	 Function which generates a Numpy histogram of the 
	 average distance (pv_true - pv_reco) per particle
	 
	 Input: a list (of the size of nPVs * nTracksPerPV) 
	 of associated reconstructed PV positions, 
	 together with a similar list but with the true PV 
	 positions per particle.
	 
	 Output: void
	"""
	hist, bins = np.histogram(offsets, bins=100)
	width = 0.7 * (bins[1] - bins[0])
	center = (bins[:-1] + bins[1:]) / 2

	#plt.bar(center, hist, align='center', width=width)
	#plt.title( "Measured delta-z" )
	#plt.xlabel(['measured PV (z) - true PV (z)'])


	# p0 is the initial guess for the fitting coefficients (A, mu and sigma above)
	p0 = [1., 0., 1.]
	
	bin_centres = (bins[:-1] + bins[1:])/2

	coeff, var_matrix = curve_fit(gauss, bin_centres, hist, p0=p0)

	# Get the fitted curve
	hist_fit = gauss(bin_centres, *coeff)
	#plt.plot(bin_centres, hist_fit, label='Fitted data')
	
	#print coeff
	# Finally, lets get the fitting parameters, i.e. the mean and standard deviation:
	print 'Fitted mean = ', coeff[1]
	print 'Fitted standard deviation = ', coeff[2]
	
	return coeff[1]

	plt.show()

def show_errors( offsets ):
	hist, bins = np.histogram(offsets, bins=250)
	width = 0.7 * (bins[1] - bins[0])
	center = (bins[:-1] + bins[1:]) / 2

	plt.bar(center, hist, align='center', width=width)
	plt.title( "Measured delta-z" )
	plt.xlabel(['measured PV (z) - true PV (z)'])


	# p0 is the initial guess for the fitting coefficients (A, mu and sigma above)
	p0 = [1., 0., 1.]
	
	bin_centres = center

	coeff, var_matrix = curve_fit(gauss, bin_centres, hist, p0=p0)

	# Get the fitted curve
	hist_fit = gauss(bin_centres, *coeff)
	plt.plot(bin_centres, hist_fit, label='Fitted data')
	
	#print coeff
	# Finally, lets get the fitting parameters, i.e. the mean and standard deviation:
	print 'Fitted mean = ', coeff[1]
	print 'Fitted standard deviation = ', coeff[2]
	
	#return coeff[1]
	plt.show()

	plt.show()

def generate_measurement_to_particle_table( xyList ):
	measurementToParticleTable = {}
	uniqueParticleId = 0
	for measurement in xyList:
		if  (measurement[0], measurement[1]) in measurementToParticleTable.keys():
			print "Double measurement-particle assignment!"
			return False

		measurementToParticleTable[ (measurement[0], measurement[1]) ] = measurementToParticleTable.get((measurement[0], measurement[1]), [])
		measurementToParticleTable[ (measurement[0], measurement[1]) ] = uniqueParticleId
		uniqueParticleId+=1
	
	return measurementToParticleTable

if __name__ == '__main__':
	nPVs = 200
	nTracksPerPV = 15
	nTrials = 5
	
	#nTracksPerPV = 5
	#errorList = [0.028174663233069028, 0.072933788723594753, -0.045267176892166514, 0.041062576226567532, 0.11841207013226242, 0.059996338631731219, 0.014971633898003352, 0.077955785194105759, 0.16591755289263505, -0.082661607477670943, 0.01446728894839347, 0.0013354105543116649, -0.12787312032550835, 0.052142646226978465, 0.087118295820160882, -0.02346020039833346, -0.0080696113670603743, 0.043430840543819849, -0.001390789201114591, 0.016353300102083863, 0.016492370902658388, 0.0097734386448741061, 0.054218446343575623, -0.080221616177271332, 0.049486177655907571, -0.017730638985001552, 0.10417511384244463, 0.038185953733749597, -0.0076389312648843435, 0.0033460079816652858, 0.0091689430933811714, 0.028993142526524809, 0.1145086498828303, 0.004990289091553966, -0.11284970031312069, 0.10070099676977776, 0.024531149892624986, -0.11018834734234084, -0.0021188192791714998, 0.051592088190899846, -0.022582971658728801, -0.042166794156873869, 0.0022414253123133354, -0.038025719367305984, 0.15332413798553055, 0.080434304333404261, -0.0059958796379234501, -0.045040352453774093, -0.094914420905526486, 0.099807550830809694]
	#errorList = [-0.0099418404651496085, -0.02176584472045278, 0.029792270535406996, 0.0015039259798021627, -0.089514778858702126, -0.0043783882703994307, 0.091776916396858949, -0.10630251059865206, -0.08267879010277851, -0.022212534274385257, -0.035656867015923577, -0.019928751438127001, -0.12792763217083206, -0.04849468046124817, 0.017501222394914778, 0.054567248594576102, -0.011763876406432554, 0.1144553550015036, 0.021598254626360031, 0.06139198654677154, 0.13242997471010926, -0.093059860577384648, -0.061770464803225136, -0.059513297578151846, 0.060665725997243271, -0.070251278943450818, -0.055611455523391175, 0.048640912625534008, 0.022209613412314512, 0.010634356691469848, 0.024705056172804281, 0.0068566837669224263, -0.088395075782300755, 0.062078895405972091, 0.052721757331927493, 0.046902364230429858, -0.027635136829159787, 0.036230238398631827, 0.04528378063952887, 0.020862605088386037, 0.057959263394360049, -0.0088278645162360638, 0.06709587683349362, -0.052933634425064664, 0.058717878374857112, -0.089374703207899531, -0.048627592440845566, -0.020279160356647199, 0.072191464791448723, 0.013552054135982858, 0.02817466323306903, 0.07293378872359475, -0.045267176892166514, 0.04106257622656753, 0.11841207013226242, 0.05999633863173122, 0.014971633898003352, 0.07795578519410576, 0.16591755289263505, -0.08266160747767094, 0.01446728894839347, 0.001335410554311665, -0.12787312032550835, 0.052142646226978465, 0.08711829582016088, -0.02346020039833346, -0.008069611367060374, 0.04343084054381985, -0.001390789201114591, 0.016353300102083863, 0.016492370902658388, 0.009773438644874106, 0.05421844634357562, -0.08022161617727133, 0.04948617765590757, -0.017730638985001552, 0.10417511384244463, 0.0381859537337496, -0.0076389312648843435, 0.0033460079816652858, 0.009168943093381171, 0.02899314252652481, 0.1145086498828303, 0.004990289091553966, -0.1128497003131207, 0.10070099676977776, 0.024531149892624986, -0.11018834734234084, -0.0021188192791715, 0.051592088190899846, -0.0225829716587288, -0.04216679415687387, 0.0022414253123133354, -0.038025719367305984, 0.15332413798553055, 0.08043430433340426, -0.00599587963792345, -0.04504035245377409, -0.09491442090552649, 0.0998075508308097, -0.048937638896441468, -0.034644711985612746, 0.064801555832572258, 0.0062222612965497671, 0.0083976450448648658, 0.018491157701113051, 0.03401749956820322, 0.0027437533544404386, -0.033210729856107325, 0.11274688934695944, -0.010889654328557406, 0.042642806515337715, 0.11524984364750909, 0.0041058485649817962, 0.01336630053337377, -0.033788807893515668, 0.030053003850597833, 0.018783378222896368, 0.061445539565621633, 0.042053118384061353, 0.052255846187577823, 0.033694745704259288, 0.069582283749645313, -0.0033689955334001657, -0.074258774200374078, -0.060861433066785757, 0.064098785075411377, -0.047164761978043937, 0.099078378340880513, -0.14997502431085066, 0.013617570865834936, 0.031819888459196546, 0.10838304948623784, -0.022909022002453833, -0.026495881952077485, -0.088539423618286345, -0.069886781815929291, 0.024147794195736028, 0.06060755346561799, 0.016826392743438678, 0.0158674327696159, -0.062283767729497293, -0.030697780477079935, -0.054681476165027859, 0.018737893577845322, 0.0073989706526624375, 0.011618927171191066, 0.051923344396504388, -0.051044713587026593, 0.039769241240963357]
	
	#nTracksPerPV = 15
	#errorList = [ 0.0750167735331, 0.039567152904766201, -0.028713566710741354, 0.029972482128640534, -0.022727118075040652, 0.051076575697265231, 0.010730217614429173, 0.045627994936148671, 0.049798618248365213, 0.025520263487048986, 0.030318123065824269, -0.033401620793488081, -0.031514650016282161, 0.023112967405366492, -0.025394023551080069, 0.0855040255843, -0.0398601091863, 0.133320373007, -0.0960788784501, -0.00703748326412, 0.0689948522699, -0.0395468167159, -0.0183733983065, -0.0374353299538, 0.0114669339448, 0.0606750283086, -0.0132524005766, 0.0021302149656, -0.007855393147, 0.0676563287515, -0.0159652187029, -0.00978478086949, -0.00080843757199, 0.00661580737888, -0.0548414363046, 0.0149367788422, -0.0153443808437, -0.0407663149569, 0.027957387905, 0.00215322520464, 0.0748195590937, -0.0211630243294, 0.063334261669794001, 0.028576446617144285, -0.066175164574307568, 0.050724698992652112, 0.023648995859251811, 0.04923631889411681, -0.014550374269139526, -0.014618504818590311, 0.023142615296122743, 0.019361104097280389, 0.055311395234247669, 0.058882322349246202, 0.044678600047438628, 0.025541505773370603, 0.055983898155210939, -0.039370965165420616, -0.041342721386806121, -0.01709513641477443, -0.061564716183281111, 0.048277194534033251, -0.032635288256631506, -0.063797219159382565, 0.053220082515853369, -0.058169263555357557, -0.02564359413110473, -0.012869083934685515, -0.031984844796748867, 0.024148258222816681, 0.0067607811937134624, 0.012493911427892216, -0.0069132337112866506, -0.047106076848496922, 0.015577980298714876, 0.0042544970359836565, -0.017172389490727344, -0.044559308047257003, 0.063136929285879939, -0.036562828485259991, 0.03334368862738691, -0.010113928322313016, -0.0027939400442845764, -0.01399622323941868, -0.0068665527719047629, -0.036699892145441712, -0.029227657813531024, 0.0089391733725719125, -0.01387275715652244, 0.046260086018780754, -0.025839671940836483, 0.013284704677869673, -0.0047836234978084081, -0.037738762961320747, -0.056481469665193205, -0.028364037462398517, -0.076509276844288834 ]
	errorList = []
	for trial in range(nTrials):
		print "Running for trial id {}".format(trial)
		event = event_generator.generate_event( nPVs, nTracksPerPV )
		xyList = []
		for pvId in range(nPVs):
			for particleId in range(nTracksPerPV):
				xyList.append( event["reconPVtime"][pvId][particleId] )
				xyList.append( event["reconVELOz"][pvId][particleId] )

		#structure: (time, Z)
	
		#true PVs
		true_pv_list = np.array( [ ( event["tList"][ pv_id ], event["zList"][ pv_id ] ) for pv_id in range(nPVs)] )
		#true_pv_list = StandardScaler().fit_transform(true_pv_list)

		#measurements
		xyList = np.reshape(np.array(xyList), (nPVs*nTracksPerPV,2))
		#xyList = StandardScaler().fit_transform(xyList)
	
		#generate a map from Measurement -> particleId
		measurementToParticleTable = generate_measurement_to_particle_table(xyList)
		
		if measurementToParticleTable == False:
			continue

		#reconstructed PVs
		reconstructed_pvs = find_centers( xyList, nPVs )
		reconstructed_pv_as_tuple_list = np.array( [ (pv[0], pv[1]) for pv in reconstructed_pvs[0] ] )
	
		#generate a map of ParticleID -> associated PV
		particle_to_associated_pv = [0] * nPVs * nTracksPerPV
		for pvId in range(len(reconstructed_pvs[1])):
			pv = reconstructed_pvs[1][pvId]
			for measurement in pv:
				particle_to_associated_pv[ measurementToParticleTable[ (measurement[0], measurement[1]) ] ] = reconstructed_pvs[0][pvId]
	
		#generate a map of ParticleID -> true PV
		particle_to_true_pv = [0] * nPVs * nTracksPerPV
		for pvId in range(nPVs):
			pv = true_pv_list[pvId]
			for measurementId in range(nTracksPerPV):
				measurement = xyList[ nTracksPerPV*pvId + measurementId ]
				particle_to_true_pv[ measurementToParticleTable[ (measurement[0], measurement[1]) ] ] = pv
	
		offsets = [ (particle_to_true_pv[uniqueParticleId][1] - particle_to_associated_pv[uniqueParticleId][1]) for uniqueParticleId in range( nPVs * nTracksPerPV )]
		errorList.extend( offsets )
		#errorList.append( generate_pull_histogram(offsets) )

		colors = plt.cm.Spectral(np.linspace(0, 1, nPVs))
	
		if nTrials == 1:
			pltOTtime = plt
			measurements = pltOTtime.scatter( xyList[:, 0], xyList[:, 1], color='b' )
			reconstructedPVs = pltOTtime.scatter(reconstructed_pv_as_tuple_list[:,0], reconstructed_pv_as_tuple_list[:,1], color='red')
			GeneratedPVs = pltOTtime.scatter(true_pv_list[:, 0], true_pv_list[:,1], color='g', marker='^')
			pltOTtime.legend([reconstructedPVs, GeneratedPVs, measurements], ['Reconstructed Particle PV', 'Generated PVs', "Measurements"])
			pltOTtime.xlabel('PV time [ps]')
			pltOTtime.ylabel('Z position [mm]')
			pltOTtime.show()
	
	if nTrials > 1:
		#print errorList
		show_errors( errorList )
		print "Mean: {}".format( np.mean([ offset**2 for offset in errorList ]) )
	#print xyList