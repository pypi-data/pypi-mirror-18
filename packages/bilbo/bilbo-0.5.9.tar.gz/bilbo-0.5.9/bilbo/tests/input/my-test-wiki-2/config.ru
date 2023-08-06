#!/usr/bin/ruby
require 'rubygems'


module Gollum
  # to require 'my_adapter':
  Gollum::GIT_ADAPTER = "rugged"
end


require 'gollum/app'
require 'cgi'

system("which git") or raise "Looks like I can't find the git CLI in your path.\nYour path is: #{ENV['PATH']}"


Gollum::Page.send :remove_const, :FORMAT_NAMES if defined? Gollum::Page::FORMAT_NAMES
# limit to one format and set allowed extensions
Gollum::Markup.formats[:markdown][:regexp] = /(?:md|markdown|ft|mmd)/

module GitHub
  module Markup
    class Markdown < Implementation
      MARKDOWN_GEMS = {
        "rmultimarkdown" => proc { |content|
          MultiMarkdown.new(content).to_html
        }
      }

      def initialize
        super(/md|markdown|ft|mmd/i)
      end

      def load
        return if @renderer
        MARKDOWN_GEMS.each do |gem_name, renderer|
          if try_require(gem_name)
            @renderer = renderer
            return
          end
        end

        raise LoadError, "no suitable markdown gem found"
      end

      def render(content)
        load
        @renderer.call(content)
      end

      def name
        "markdown"
      end

    private
      def try_require(file)
        require file
        true
      rescue LoadError
        false
      end
    end
  end
end


module Gollum
  class Macro
    class PageMatch < Gollum::Macro
      def render(title="Pages", toc_root_path = "")
        if title != ""
          title = title+"<br>"
        end
        base_path = @wiki.base_path
        if toc_root_path[0] === "/" and toc_root_path[-1] === "/"
            toc_root_path = Regexp.new(toc_root_path[1..-2])
        end
        if @wiki.pages.size > 0
          result = @wiki.pages.map {|p|
          if toc_root_path.match(p.path)
              matches = toc_root_path.match(p.path).captures
              g1 = matches[0]
              g1 = g1.gsub '-', ' '
              "<a href=\"#{base_path}/#{p.url_path}\">#{g1}</a><br>"
          end
    }.join
        end
        if result.length > 3
          "<div><strong>#{title}</strong>#{result}</div>"
        else
          "<div><strong>No #{title}</strong></div>"
        end
      end
    end
  end
end

module Gollum
  class Macro
    class FileMatch < Gollum::Macro
      def render(title="Files",toc_root_path = "")
        if title != ""
          title = title+"<br>"
        end
        base_path = @wiki.base_path
        if toc_root_path[0] === "/" and toc_root_path[-1] === "/"
            toc_root_path = Regexp.new(toc_root_path[1..-2])
        end
        if @wiki.files.size > 0
          result = @wiki.files.map {|f|
          if toc_root_path.match(f.path)
              matches = toc_root_path.match(f.path).captures
              g1 = matches[0]
              g1 = g1.gsub '-', ' '
              "<a href=\"#{base_path}/#{f.path}\">#{g1}</a><br>"
          end
    }.join
        end
        if result.length > 3
          "<div><strong>#{title}</strong>#{result}</div>"
        else
          "<div><strong>No #{title}</strong></div>"
        end
      end
    end
  end
end

module Gollum
  class Macro
    class ParentDirectory < Gollum::Macro
      def render()
        this = ::File.dirname(@page.path)
        "#{this}"
      end
    end
  end
end

module Gollum
  class Macro
    class Attachments < Gollum::Macro
      def render(title="Attachments",parentPage = 0)
        if title != ""
          title = title+"<br>"
        end
        base_path = @wiki.base_path
        if parentPage == 0
          thisPage = @page
        else
          thisPage = @page.parent_page
        end
        parent = ::File.dirname(thisPage.path)
        regex = parent+"\/([^/]*)$"
        toc_root_path = Regexp.new(regex)
        if @wiki.files.size > 0 and thisPage.path != "projects/home.md"
          result = @wiki.files.map {|f|
          if toc_root_path.match(f.path)
              matches = toc_root_path.match(f.path).captures
              g1 = matches[0]
              g1 = g1.gsub '-', ' '
              "<a href=\"#{base_path}/#{f.path}\">#{g1}</a><br>"
          end
    }.join
        end
        if thisPage.path != "projects/home.md"
          if result.length > 3
            "<BR><div><strong>#{title}</strong>#{result}</div>"
          elsif thisPage.path != "projects/home.md"
            "<BR><div><strong>No #{title}</strong></div>"
          end
        end
      end
    end
  end
end

module Gollum
  class Macro
    class SubFolders < Gollum::Macro
      def render(title="Sub-Directories",parentPage = 0)
        if title != ""
          title = title+"<br>"
        end
        base_path = @wiki.base_path
        if parentPage == 0
          thisPage = @page
        else
          thisPage = @page.parent_page
        end
        parent = ::File.dirname(thisPage.path)
        regex = parent+"\/(.*?)\/Home"
        toc_root_path = Regexp.new(regex)
        if @wiki.pages.size > 0 and thisPage.path != "projects/home.md"
          result = @wiki.pages.map {|p|
          if toc_root_path.match(p.path)
              matches = toc_root_path.match(p.path).captures
              g1 = matches[0]
              g1 = g1.gsub '-', ' '
              g1 = g1.gsub '_', ' '
              "<a href=\"#{base_path}/#{p.url_path}\">#{g1}</a><br>"
          end
    }.join
        end
        if thisPage.path != "projects/home.md"
          if result.length > 3
            "<BR><div><strong>#{title}</strong>#{result}</div>"
          elsif thisPage.path != "projects/home.md"
            "<BR><div><strong>No #{title}</strong></div>"
          end
        end
      end
    end
  end
end

module Gollum
  class Macro
    class Tags < Gollum::Macro
      def render(parentPage = 0)
        base_path = @wiki.base_path
        if parentPage == 0
          thisPage = @page
        else
          thisPage = @page.parent_page
        end
        meta = thisPage.metadata
        if meta
          tags = meta['tags']
          if tags
            tags = tags.split(",")
            allTags = ""
            for tag in tags
              tag =tag.strip
              if !['#not-blogged', '#blogged', '#untagged'].include? tag 
                tagUrl =CGI.escape(tag)
                tag="<a href=\"#{base_path}/search?q=#{tagUrl}\">#{tag}</a>"
                allTags =allTags+ " "+tag
              end
            end
          else
            tags = ""
            allTags = ""
          end
        else
          tags = ""
          allTags = ""
        end
        if allTags != ""
          "<div style=\"text-align:right;\">#{allTags}</div><hr>"
        else
          ""
        end
      end
    end
  end
end

module Gollum
  class Macro
    class PageName < Gollum::Macro
      def render()
        name = @page.name
        this = @page.parent_page.name
        "#{name}<BR><BR><BR><BR>#{this}"
      end
    end
  end
end

module Gollum
  class Macro
    class ProjectHome < Gollum::Macro
      def render()
        base_path = @wiki.base_path
        thisPage = @page.parent_page
        regex = Regexp.new("(projects\/(.*?))\/.*")
        if regex.match(thisPage.path)
          matches = regex.match(thisPage.path).captures
          g1 = matches[0]
          g2 = matches[1]
          homeLink="<a href=\"#{base_path}/#{g1}/Home\">Home</a>"
          taskLink="<a href=\"#{base_path}/#{g1}/#{g2}\">Tasks & Logs</a>"
          title = g2.gsub '-', ' '
          title = title.gsub '_', ' '
          "<BR><div><strong>#{title}</strong><BR>#{homeLink}<br>#{taskLink}</div>"
        end
      end
    end
  end
end


module Gollum
  class Macro
    class ExternalPageLink < Gollum::Macro
      def render(baseUrl="",text="external link")
        thisPage = @page.parent_page.path
        thisPage = thisPage.strip
        "<a href=\"#{baseUrl}/#{thisPage}\">#{text}</a>"
      end
    end
  end
end



gollum_path = '/misc/pessto/dryx/qub_gollum' # CHANGE THIS TO POINT TO YOUR OWN WIKI REPO
disable :run
configure :development, :staging, :production do
 set :raise_errors, true
 set :show_exceptions, true
 set :dump_errors, true
 set :clean_trace, true
end
$path = gollum_path
Precious::App.set(:gollum_path, gollum_path)


# Specify the wiki options.
wiki_options = {
  :allow_uploads => true,
  :allow_editing => true,
  :mathjax => true,
  :h1_title => true,
  :show_all => true,
  :user_icons => "gravatar",
  :collapse_tree => true,
  :live_preview => false,
  :allow_uploads => "page",
  :universal_toc => false,
  :css => true,
  :js =>  false,
  :adapter => "rugged"
}
Precious::App.set(:wiki_options, wiki_options)


# Set as Sinatra environment as production (no stack traces)
Precious::App.set(:environment, :production)

# Setup Omniauth via Omnigollum.
require 'omnigollum'
require 'omniauth-google-oauth2'


options = {
  # OmniAuth::Builder block is passed as a proc
  :providers => Proc.new do
    provider :google_oauth2, "621317204570-m4bcdj3jhn3m7g7s6ap9or6hr4usf5q9.apps.googleusercontent.com","L4zODtbu28B1b0BTvMj3bg-b", skip_jwt: true
    {
      #:prompt => "select_account",
      :image_aspect_ratio => "square",
      :image_size => 50
    }
  end,
  :dummy_auth => false,
  # Make the entire wiki private
  :protected_routes => ['/*'],
  # Specify committer name as just the user name
  :author_format => Proc.new { |user| user.name },
  # Specify committer e-mail as just the user e-mail
  :author_email => Proc.new { |user| user.email }
}

options[:authorized_users] = ["davidrobertyoung@gmail.com"]

# :omnigollum options *must* be set before the Omnigollum extension is registered
Precious::App.set(:omnigollum, options)
Precious::App.register Omnigollum::Sinatra


## ADAPT SANITIZATION
sanitizer = Gollum::Sanitization.new
sanitizer.protocols['a']['href'].concat ['subl'] # Protocols
# sanitizer.elements.concat ['customtag1', 'customtag2'] # Tags
sanitizer.attributes['img'].push 'style' # Attributes
Precious::App.set(:sanitization, sanitizer)


map '/dry/wiki' do
    run Precious::App
end
