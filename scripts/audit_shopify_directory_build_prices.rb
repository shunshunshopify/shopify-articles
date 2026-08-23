#!/usr/bin/env ruby

require "cgi"
require "net/http"
require "thread"
require "uri"

source_path = ARGV.fetch(0, "drafts/shopify-development-companies-source-data.md")
text = File.read(source_path, encoding: "UTF-8")

companies = text.scan(/^## (\d+)\. (.+?)\n.*?^- Shopify Partner Directory: (https:\/\/www\.shopify\.com\/partners\/directory\/partner\/\S+)/m).map do |number, name, url|
  { number: number.to_i, name: name, url: url }
end

queue = Queue.new
companies.each { |company| queue << company }
results = Queue.new

workers = 8.times.map do
  Thread.new do
    while (company = queue.pop(true) rescue nil)
      begin
        uri = URI(company[:url])
        response = Net::HTTP.get_response(uri)
        body = response.body.to_s
        body.gsub!(/<script\b.*?<\/script>/mi, " ")
        body.gsub!(/<style\b.*?<\/style>/mi, " ")
        visible = CGI.unescapeHTML(body.gsub(/<[^>]+>/, " ").gsub(/\s+/, " "))
        specialized = visible[/Specialized services(.*?)(?:Other services|Industries|Featured work|Rating)/m, 1].to_s
        price = specialized[/Store build or redesign\s+(Starting at \$[\d,]+|Contact for pricing)/, 1]
        results << company.merge(price: price || "掲載価格なし")
      rescue StandardError => error
        results << company.merge(price: "取得失敗: #{error.class}")
      end
    end
  end
end

workers.each(&:join)

puts "No.\t企業\tStore build or redesign\tDirectory"
results.size.times.map { results.pop }.sort_by { |row| row[:number] }.each do |row|
  puts [row[:number], row[:name], row[:price], row[:url]].join("\t")
end
