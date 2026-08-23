#!/usr/bin/env ruby

require "cgi"
require "net/http"
require "thread"
require "uri"

html_path = ARGV.fetch(0, "drafts/shopify-development-companies-50.html")
html = File.read(html_path, encoding: "UTF-8")

rows = (1..50).map do |number|
  start_at = html.index(%(<h3 id="company-#{number}"))
  next unless start_at
  end_marker = number < 50 ? %(<h3 id="company-#{number + 1}") : "<h2"
  end_at = html.index(end_marker, start_at + 1) || html.length
  block = html[start_at...end_at]
  name = block[/調査No\.#{number}\s+([^<]+)/, 1]
  cases = block[/<strong>Shopify構築実績：<\/strong>(.*?)<\/li>/m, 1].to_s
               .gsub(/<[^>]+>/, " ").gsub(/&amp;/, "&").gsub(/\s+/, " ").strip
  source_url = block[/<strong>実績確認元：<\/strong><a href="([^"]+)/, 1]
  { number: number, name: name, first_case: cases.split("、").first.to_s, source_url: source_url }
end.compact

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
rows.each { |row| queue << row }
results = Queue.new

workers = 8.times.map do
  Thread.new do
    while (row = queue.pop(true) rescue nil)
      if row[:first_case] == "公開情報では確認できず" || row[:source_url].to_s.empty?
        results << row.merge(status: "未掲載", found: "-")
        next
      end
      begin
        code, resolved_url, visible = fetch_visible(row[:source_url])
        candidates = [
          row[:first_case],
          row[:first_case].sub(/（.*\z/, "").strip,
          row[:first_case].split(/[／|]/).last.to_s.strip
        ].reject(&:empty?).uniq
        matched = candidates.find { |candidate| visible.downcase.include?(candidate.downcase) }
        results << row.merge(status: code, found: matched ? "yes" : "no", resolved_url: resolved_url)
      rescue StandardError => error
        results << row.merge(status: "取得失敗: #{error.class}", found: "-")
      end
    end
  end
end

workers.each(&:join)

puts "No.\t企業\t導入実績①\tHTTP\t根拠ページ内一致\t確認元"
results.size.times.map { results.pop }.sort_by { |row| row[:number] }.each do |row|
  puts [row[:number], row[:name], row[:first_case], row[:status], row[:found], row[:resolved_url] || row[:source_url]].join("\t")
end
