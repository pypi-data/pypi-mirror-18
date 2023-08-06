:

tmp=/tmp/$$_
trap "rm ${tmp}; exit 0" 0 1 2 15

#
#
#

ZONE=${1-example.com}
ZONE_ID=`cli4 name="${ZONE}" per_page=1 /zones | jq '.id'`

#
# A "monitor" defines the parameters for a health monitor which
# periodically checks the availability of a single origin IP address
# by making network requests to a network endpoint (the monitored
# endpoint).
# It is associated with an "origin pool", specifying how to monitor
# all the origin IP addresses contained in the associated origin pool.
#

	ATTRIBUTES= \
		expected_codes="2xx" \
		interval=60 \
		retries=2 \
		path="/cf-poll-status" \
		type="http"
	cli4 --post ${ATTRIBUTES} /user/load_balancers/monitors > ${tmp}
	monitor_id=`jq '.id' < ${tmp}`
	echo "monitor: ${monitor_id}"

#
# A "notifier" defines the parameters used to deliver a notification
# message when a change in origin health status has been detected.
#

	ATTRIBUTES= \
		type="email" \
		address="mahtin@mahtin.com"

	cli4 --post ${ATTRIBUTES} /user/load_balancers/notifiers > ${tmp}
	notifier_id=`jq '.id' < ${tmp}`
	echo "notifier: ${notifier_id}"

#
# An "origin" defines a single origin IP address which is proxied by
# Cloudflare (or resolved directly to the internet in the case of
# "grey clouded" operation) and to which the CTM balances traffic.
# Origins are grouped into "pools" and an origin will never receive
# traffic if it is not associated with a pool.
#

	ATTRIBUTES= \
		name="www-little-rock-1" \
		description="Little Rock" \
		address="50.193.229.169" \
		notifier="${notifier_id}"
	cli4 --post ${ATTRIBUTES} /user/load_balancers/origins > ${tmp}
	origin1_id=`jq '.id' < ${tmp}`
	echo "origin: ${origin1_id}"

	ATTRIBUTES= \
		name="www-little-rock-2" \
		description="Little Rock" \
		address="50.193.229.168" \
		notifier="${notifier_id}"
	cli4 --post ${ATTRIBUTES} /user/load_balancers/origins > ${tmp}
	origin2_id=`jq '.id' < ${tmp}`
	echo "origin: ${origin2_id}"

#
# A "pool" groups a number of origins in order to treat them as a unit
# where it pertains to certain functional aspects of the CTM. For
# example, when the number of healthy origins in a pool decreases below
# a configurable threshold, the entire pool is considered to be
# unavailable and traffic will not be directed to any origins inside
# the pool. Instead, traffic usually destined for origins in the
# unavailable pool will be directed to another pool (configured on a
# geographic basis).
#

	ATTRIBUTES= \
		name="usa-pool" \
		origins="[ ${origin2_id} , ${origin2_id} ]" \
		notifier="${notifier_id}" \
		monitor="${monitor_id}"
	cli4 --post ${ATTRIBUTES} /user/load_balancers/pools > ${tmp}
	pool_id=`jq '.id' < ${tmp}`
	echo "pools: ${pool_id}"

#
# A "location mapping" associates a list of pools with a particular
# geographic region, indicating the precedence in which traffic should
# be routed across the different pools from a particular geographic
# region. There is also a "global" mapping, which applies in the absence
# of any health information being available.
#

	ATTRIBUTES= \
		global_pools="[ "${pool_id}" ]" \
		region_pools="[ ]"
	cli4 --post ${ATTRIBUTES} /user/load_balancers/maps > ${tmp}
	map_id=`jq '.id' < ${tmp}`
	echo "map: ${map_id}"

#
# A Global Policy specifies the global routing policy as well as the
# associated location mapping.
#

	ATTRIBUTES= \
		location_mapping="${map_id}"
		notifier="${notifier_id}"
		fallback_pool="${pool_id}"
	cli4 --post ${ATTRIBUTES} /user/load_balancers/global_policies > ${tmp}
	global_policy_id=`jq '.id' < ${tmp}`
	echo "global_policy: ${global_policy_id}"

#
# Create a Load Balancer, and attach our Global Policy.
#

	ATTRIBUTES= \
		name="www.${ZONE}", \
		global_policy="${pool_id}", \
		proxied=true
	cli4 --post ${ATTRIBUTES} /zone/:${ZONE}/load_balancers > ${tmp}
	load_balancer_id=`jq '.id' < ${tmp}`
	echo "load_balancer: ${load_balancer_id}"

# WNAM	; Western North America
# ENAM	; Eastern North America
# EU	; Europe
# NSAM	; Northern South America
# SSAM	; Southern South America
# OC	; Oceania
# ME	; Middle East
# NAF	; Northern Africa
# SAF	; Southern Africa
# IN	; India
# SEAS	; Southeast Asia
# NEAS	; Northeast Asia
# CHINA	; China

	REGION=ENAM

	ATTRIBUTES= \
		"[ ${pool_id} ]"
	cli4 --put ${ATTRIBUTES} /user/load_balancers/maps/${map_id}/region/:${REGION}
	map_region_id=`jq '.id' < ${tmp}`
	echo "map_region: ${map_region_id}"

#
# List all the maps ...
#
	cli4 --get /user/load_balancers/maps/${map_id}

