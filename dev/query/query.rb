require 'net/http'
require 'nokogiri'
require 'levenshtein'

def countGoogleQueryFilteringTitleByLevenshtein(query)
	doc 	= Nokogiri::HTML(Net::HTTP.get('www.google.com', "/search?q=#{URI::encode(query)}"))
	titles 	= doc.css('h3.r a').map { |n| n.inner_text }

	count = 0
	titles.each do |i|	
		title = i.encode("UTF-8", 'binary', :invalid => :replace, :undef => :replace, :replace => "?")
		title.split(/\W+/).each do |word|
			distance = Levenshtein.distance(query, word)
			count += 1 if distance <= 2
		end
	end
	return count
end

#puts "Type query and press enter:"
puts countGoogleQueryFilteringTitleByLevenshtein(gets.chomp)