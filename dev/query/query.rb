require 'net/http'


def levenshtein(a, b)
	return a.length if (b.length == 0)
	return b.length if (a.length == 0)

	m = Array.new(a.length+1) { Array.new (b.length+1) }
	(0..a.length).each { |i| m[i][0] = i }
	(0..b.length).each { |j| m[0][j] = j }

	for i in (1..a.length) do
		for j in (1..b.length) do
			m[i][j] = [ m[i  ][j-1] + 1, 
						m[i-1][j  ] + 1, 
						m[i-1][j-1] + ( a[i-1] == b[j-1] ? 0 : 1 ) ].min
		end
	end

	return m[a.length][b.length]
end


def getTitlesFromGoogleQuery(query)
	html  = Net::HTTP.get('www.google.com', "/search?q=#{URI::encode(query)}")
	parts = html.split("<h3 class=\"r\">")
	htmlTitles = parts[1, parts.length]								   # O primeiro pedaço html é besteira, ficamos apenas com o restante
	htmlTitles = htmlTitles.collect{ |x| x[0, x.index("</a>")] }	   # Queremos apenas o texto na primeira tag <a>
	textTitles = htmlTitles.collect{ |x| x.gsub(%r{</?[^>]+?>}, '') }  # Excluimos as tags html dessa parte ...
end


def countGoogleQueryFilteringTitleByLevenshtein(query)	
	titles = getTitlesFromGoogleQuery(query)
	count  = 0
	titles.each do |i|	
		title = i.encode("UTF-8", 'binary', :invalid => :replace, :undef => :replace, :replace => "?")
		title.split(/\W+/).each do |word|
			distance = levenshtein(query, word)
			count += 1 if distance <= 2
		end
	end
	return count
end


#puts "Type query and press enter:"
puts countGoogleQueryFilteringTitleByLevenshtein(gets.chomp)
