:

tmp=/tmp/$$_
trap "rm ${tmp}; exit 0" 0 1 2 15

PAGE=0

while true
do
	cli4 --raw per_page=5 page=${PAGE} /zones > ${tmp}

	domains=`jq -c '.|.result|.[]|.name' < ${tmp} | tr -d '"'`
	result_info=`jq -c '.|.result_info' < ${tmp}`

	COUNT=`      echo "${result_info}" | jq .count`
	PAGE=`       echo "${result_info}" | jq .page`
	PER_PAGE=`   echo "${result_info}" | jq .per_page`
	TOTAL_COUNT=`echo "${result_info}" | jq .total_count`
	TOTAL_PAGES=`echo "${result_info}" | jq .total_pages`

	echo COUNT=${COUNT} PAGE=${PAGE} PER_PAGE=${PER_PAGE} TOTAL_COUNT=${TOTAL_COUNT} TOTAL_PAGES=${TOTAL_PAGES} -- ${domains}

	if [ "${PAGE}" == "${TOTAL_PAGES}" ]
	then
		## last section
		break
	fi

	# grab the next page
	PAGE=`expr ${PAGE} + 1`
done

