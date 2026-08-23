#!/usr/bin/env ruby

require "cgi"
require "net/http"
require "thread"
require "uri"

source_path = ARGV.fetch(0, "drafts/shopify-development-companies-source-data.md")
text = File.read(source_path, encoding: "UTF-8")

companies = text.scan(/^## (\d+)\. (.+?)\n(.*?)(?=^## \d+\.|\z)/m).map do |number, name, block|
  {
    number: number.to_i,
    name: name,
    official_url: block[/^- 公式サイト: (\S+)/, 1],
    directory_url: block[/^- Shopify Partner Directory: (\S+)/, 1]
  }
end

companies.each do |company|
  company[:official_url] = "https://www.dentsudigital.co.jp/" if company[:number] == 23
end

def fetch_visible(url)
  uri = URI(url)
  response = Net::HTTP.get_response(uri)
  redirects = 0
  while response.is_a?(Net::HTTPRedirection) && redirects < 5
    uri = URI.join(uri, response.fetch("location"))
    response = Net::HTTP.get_response(uri)
    redirects += 1
  end
  body = response.body.to_s.force_encoding("UTF-8").encode("UTF-8", invalid: :replace, undef: :replace, replace: " ")
  body.gsub!(/<script\b.*?<\/script>/mi, " ")
  body.gsub!(/<style\b.*?<\/style>/mi, " ")
  body.gsub!(/<!--.*?-->/m, " ")
  visible = CGI.unescapeHTML(body.gsub(/<[^>]+>/, " ").gsub(/\s+/, " "))
  [response.code, uri.to_s, visible]
end

queue = Queue.new
companies.each { |company| queue << company }
results = Queue.new

workers = 8.times.map do
  Thread.new do
    while (company = queue.pop(true) rescue nil)
      begin
        official_code, resolved_url, official_text = fetch_visible(company.fetch(:official_url))
        directory_code, _directory_resolved, directory_text = fetch_visible(company.fetch(:directory_url))
        results << company.merge(
          official_code: official_code,
          resolved_url: resolved_url,
          official_shopify: official_text.match?(/shopify/i),
          official_ec: official_text.match?(/(?:EC|e-commerce|ecommerce|オンラインストア)/i),
          directory_code: directory_code,
          directory_build: directory_text.include?("Store build or redesign"),
          directory_migration: directory_text.include?("Store migration")
        )
      rescue StandardError => error
        results << company.merge(error: error.class.to_s)
      end
    end
  end
end

workers.each(&:join)

puts "No.\t企業\t公式HTTP\t公式にShopify\t公式にEC\tDirectory HTTP\tStore build\tStore migration\t最終URL"
results.size.times.map { results.pop }.sort_by { |row| row[:number] }.each do |row|
  if row[:error]
    puts [row[:number], row[:name], "取得失敗: #{row[:error]}", "-", "-", "-", "-", "-", row[:official_url]].join("\t")
    next
  end
  puts [
    row[:number], row[:name], row[:official_code], row[:official_shopify] ? "yes" : "no",
    row[:official_ec] ? "yes" : "no", row[:directory_code], row[:directory_build] ? "yes" : "no",
    row[:directory_migration] ? "yes" : "no", row[:resolved_url]
  ].join("\t")
end
