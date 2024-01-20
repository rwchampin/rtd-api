import json, re, requests, base64
from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
from openai import OpenAI
from .models import BlogTopic, PostType, Tag, BlogPost
from django.core.files.base import ContentFile

from django.utils.text import slugify

class Assistant:
    # init function
    def __init__(self, model_type='gpt-3.5-turbo'):
        self.client = OpenAI(api_key='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')
        
        self.model = "gpt-3.5-turbo-1106"
        
        self.primary_keyword = ''
        self.supporting_keywords = []
        
        self.company_info = 'You are a genius assistant for a tech company called, Importlio, who is building a website & app containing a set of tools to benefit dropshipping shopify users. Keep seo phrases, words & best practices that will benefit this sort of company when answering any and all questions.'
        self.system_messages = {
            # add vars to strings
            'title': 'The titles first word MUST be the primary keyword,' + self.primary_keyword + ' and also contain one of the supporting keywords:' + ','.join(self.supporting_keywords) + '.  The title must be under 60 characters.',
            'subtitle': 'The subtitle should have 2 or more seo keywords in it and the first word must be one of the keywords.  Try to keep this subtitle under 60 characters.',
            'excerpt': 'The excerpt should have 2 or more seo keywords in it and the first word must be one of the keywords.  Try to keep this excerpt under 60 characters.',
            'REPHRASE': 'You will parse large strings of html and rewrite/rephrase the inner text of the html so that it is totally unique.  you will return a totally rewritten string containing the same html, and NEW unique inner text of the html.  You will rewrite the inner text while keeping the same overall concept of the initial topic.   You will return me a new string containing the html tags and the newly written inner text.  For example you will be given a string such as: `<section><h2>How to make a website</h2><p>First you need to learn HTML, CSS, and Javascript.</p></section>` and you will return a new string such as: `<section><h2>Building Websites: A comprehensive guide</h2><p>Building websites requires three primary skillsets.  They are HTML,CSS & javascript.</p></section>`.  The strings of html i provide you will often be more complex, with nested html structures that will require you to use your best judgement of the overall topic.',
            'basic_assistant': 'You are a helpful assistant that helps me by answering my questions.',
        }

    # function to set the model
 
    
    def add_user_message(self, message):
        m = {}
        m['role'] = 'user'
        m['content'] = message
        self.messages.append(m)
        
    def add_assistant_message(self, message):
        m = {}
        m['role'] = 'assistant'
        m['content'] = message
        self.messages.append(m)
    
    def create_message(self, role, content):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
        )
        import pdb; pdb.set_trace()
        return response.choices[0].text
    
    def get_info(self):
        for m in self.client.models.list():
            print(m)

 
            
    def set_model(self, model):
        self.model = AssistantModel.objects.get(name=model)
        self.set_token_encoding()

    def set_token_encoding(self):
        self.token_encoding = tiktoken.encoding_for_model(self.model.name)
        
    def get_token_count(self, text):
        return len(self.token_encoding.encode(text))
    
    def set_max_tokens(self, max_tokens):
        self.max_tokens = max_tokens
        
    def valid_text_size(self, text):
        c = self.get_token_count(text)
        if (c*2) > self.max_tokens:
            return False
        return True
    
    def create_title(self, title):
        # I WRITE A DETAILED PROMPT BASED ON MY NEEDS AND ASK FOR A NEW UNIQUE TITLE
        print('create title')
        prompt = 'You will receive a title for a blog post.  You will rewrite the title so that it is totally unique. The title must be under 60 characters.  You will return a json object containing the title. The json object will look like: {title: my title}.'
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "user", "content": prompt },
            ]
        )

        res = response.choices[0].message.content
        print(json.loads(res)['title'])
        return json.loads(res)['title']
    
    def create_subtitle(self, data):
        # SAME THING BUTASUBTITLE
        print('create subtitle')
        prompt = self.company_info + ' you must write a seo focused subtitle for a blog post with the title: ' + data['title'] + ' and a primary keyword of: ' + self.primary_keyword + ' and supporting keywords of: ' + ','.join(self.supporting_keywords) + ' and a summary of: ' + self.summary + '.  The subtitle must be under 60 characters. The subtitle must use the primary kew word and use 1-3 supporting keywords.  You will return a json object containing the subtitle. The json object will look like: {subtitle: my subtitle}.'
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "user", "content": prompt },
            ]
        )

        res = response.choices[0].message.content
        
        return json.loads(res)['subtitle']
    
    def create_excerpt(self, data):
        
        print('create excerpt')
        prompt = self.company_info + ' you must write a seo focused excerpt for a blog post with the title: ' + data['title'] + ' and a primary keyword of: ' + self.primary_keyword + ' and supporting keywords of: ' + ','.join(self.supporting_keywords) + ' and a summary of: ' + self.summary + '.  The excerpt must be greater than 100 characters under 160 characters. The excerpt must use the primary kew word as the first word and use 3-5 supporting keywords.  You will return a json object containing the excerpt. The json object will look like: {excerpt: my excerpt}.'
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "user", "content": prompt },
            ]
        )

        res = response.choices[0].message.content
        
        return json.loads(res)['excerpt']
    
    def create_headline(self, data):
        print('create headline')
        prompt = self.company_info + ' you must write a seo focused headline for a blog post with the title: ' + data['title'] + ' and a primary keyword of: ' + self.primary_keyword + ' and supporting keywords of: ' + ','.join(self.supporting_keywords) + ' and a summary of: ' + self.summary + '.  The headline must be under 5 words long. The headline is a small title that goes above the main title, as kind of an intro to the title. You will return a json object containing the headline. The json object will look like: {headline: my headline}.'
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "user", "content": prompt },
            ]
        )

        res = response.choices[0].message.content
        
        return json.loads(res)['headline']
    
    def create_shadowText(self, data):
        print('create shadowText')
        prompt = self.company_info + ' you must write a seo focused shadowText for a blog post with the title: ' + data['title'] + ' and a primary keyword of: ' + self.primary_keyword + ' and supporting keywords of: ' + ','.join(self.supporting_keywords) + ' and a summary of: ' + self.summary + '.  The shadowText must be under 5 words long. The shadowText is a small title the is mainly for visual effect and is rotated sideways and positioned fixed on the left of the screen with an opaque effect but still has seo ranking possibilty.  The shadowtext title should have at least 1 seo keyword and be 3-5 words long. You will return a json object containing the shadowText. The json object will look like: {shadowText:  my shadowText}.'
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "user", "content": prompt },
            ]
        )

        res = response.choices[0].message.content
        
        return json.loads(res)['shadowText']
    
    def create_seo_keywords(self):
        print('create seo keywords')
        prompt = self.company_info + ' you must write a list of seo meta keywords for a blog post with a primary keyword of: ' + self.primary_keyword + ' and supporting keywords of: ' + ','.join(self.supporting_keywords) + ' and a summary of: ' + self.summary + '. The list must me between 25-50 individual items.  An item can be either a single word or it can be a phrase.  Be sure to use the current primary and supporting keywords and build off of them to make the best possbile seo list.  You will return a json object containing the seo_keywords. The json object will look like: {seo_keywords:  [key1, key2, key3]}.'
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "user", "content": prompt },
            ]
        )

        res = response.choices[0].message.content
        
        return json.loads(res)['seo_keywords']
     
    def create_details(self, soup):
        # THIS FN TAKES THE TITLE TAG OF THE PAGE, AND OTHER META DATA,
        # AND SENDS IT TO OPENAI WITH A PROMPT TELLING IT TO USE THE TITLE, DESCRIPTION 
        # AND MAKEME A NEWTITLE, SUBTITLE, EXCERPT, HEADLINE, SHADOWTEXT, SEO_TITLE, SEO_DESCRIPTION, SEO_KEYWORDS
        title = soup.title.string
         # if description is present, get its inner text
        x = soup.select('meta[name="description"]')
        # if x is not empty, get the content
        if x:
            description = x[0].attrs["content"]
        
        post_content = soup.find('div', attrs={'class': 'post-content'})
        text = post_content.get_text()

        # split the text into chunks of 5000 characters
        data = {}
        data['seo_keywords'] = []
        data['summaries'] = []
        # THIS IS A BIT CUSTOM AND NOT NEEDED BUT I TOTALLY REMOVE ALL THE HTML HERE AND CHUNK IT TO OPEN AI TO HELP IT MAKE
        # ME AN OVERALL SUMARY FOR AN EXCERPT AMONG OTHER THINGS.
        chunks = split_string_with_limit(text, self.max_tokens/2, self.token_encoding)

        # NOW I LOOP OVER EACH CHUNK AND SEND IT TO OPEN AI TO GET AN OVERALL SUMMARY
        for chunk in chunks:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": self.company_info + " you will recieve a chunk of text for a long blog post. Analyze the text and identify as many seo keywords or topics we can use to rank better on google for words and phrases that will benefit a shopify dropshipping app company.  You will also return an extensive summary of everyhing mentioned in the text to help us make additional data about the post.  You will return a json object containing the seo_keywords and summaries. The json object will look like: {seo_keywords: ['keyword1', 'keyword2', 'keyword3'], summaries: ['summary1', 'summary2', 'summary3']}.  You will use the data I provide to calculate the best possible single answer for each." }, 

                    {"role": "user", "content": str(chunk)}
                ]
            )
            res = response.choices[0].message.content
            res = json.loads(res)
            data['seo_keywords'] = data['seo_keywords'] + res['seo_keywords']
            data['summaries'] = data['summaries'] + res['summaries']

            # CURRENTLY, I DONT RLY USE THE SUMMARY, BUT I USE THIS TO GENERATE A LIST OF SEO KEYWORDS
         

        # HERE IS MY OVERALL POST OBJ.
        # I SPLIT IT UP INTO INDIVIDUAL FUNCTIONS TO MAKE EACH VITAL PART OF MY POST MODEL
        post = {}
        post['title'] = self.create_title(data)
        post['subtitle'] = self.create_subtitle(data)
        post['excerpt'] = self.create_excerpt(data)
        post['headline'] = self.create_headline(data)
        post['shadowText'] = self.create_shadowText(data)
        post['seo_title'] = self.create_seo_title(data)
        post['seo_description'] = self.create_seo_description(data)
        post['seo_keywords'] = self.create_seo_keywords(data)

        # ALL OF THESE FUNCTIONS ARE SPECIFIC FOR MY POST MODEL BUT WHAT YOU DO HERE IS SEND DATA TO CHAT GPT TO CALCULATE NEW DATA YOU WANT.
        
        return post
    
    
    def create_main_info(self, soup):
        print('create main info')

    def calculate_keyword_frequency(self, words):

        # Count the frequency of each word
        word_freq = Counter(words)

        # Return the most common keyword
        most_common_keyword = word_freq.most_common(1)

        return most_common_keyword[0] if most_common_keyword else None

    def create_core_data(self):
        cleaned_text = self.soup.get_text()

        # Convert to lowercase
        cleaned_text = cleaned_text.lower()
        
        # Remove special characters and non-alphabetic characters
        cleaned_text = re.sub(r'[^a-zA-Z\s]', '', cleaned_text)

        # Remove extra spaces and line breaks
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()


        # Remove stop words
        stop_words = set(stopwords.words('english'))
        words = cleaned_text.split()
        filtered_words = [word for word in words if word not in stop_words]
        cleaned_text = ' '.join(filtered_words)
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content":self.company_info +  "You will be givin a large string of text for a blog post based on one of the companies many features and target search terms. You will also get the posts primary keyord:" + self.primary_keyword + ". You will analyze the text identify & use the primary keyword to  base everything else off of. You will summarize the entire given text into the smallest paragrapgh sized summary you can, that captures all important topics of the text and aligns with the primary keyword.  You will return a json object containing the summary, and supporting_keywords. The json object will look like: {summary: 'short summary', supporting_keywords: ['keyword2', 'keyword3']}.  You will use the data I provide to calculate the best possible single answer for each." },
                {"role": "user", "content": cleaned_text}
            ]
        )

        res = json.loads(response.choices[0].message.content)
        self.supporting_keywords = res['supporting_keywords']
        self.summary = res['summary']
        self.cleaned_text = cleaned_text

        print('supporting keywords',self.supporting_keywords)
        print('summary',self.summary)
        if self.supporting_keywords:
            return True
        return False
       
        
    def create_image(self, content):
        print('create image')
        prompt = self.company_info + 'You will receive a large string of text for a section of a blog post.  Create an image based on the given text.  The image will be the image for that section of the blog post.'
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            n=1  # Specify the number of images to generate
        )

        img_url = response.data[0].url

        # Download the image
        img_response = requests.get(img_url)
        img_data = BytesIO(img_response.content)

        # Open the image using PIL
        img = Image.open(img_data)

        # Convert the image to base64
        buffered = BytesIO()
        img.save(buffered, format="PNG")  # You can choose a different format if needed
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return img_base64
            
    
    def create_content(self):
        print('create content')
        p = ''
        for keyword in self.supporting_keywords:

            prompt = self.company_info + 'You will receive a keyword & a large string of text for a blog post based on one of the companies many features and target search terms.  You will analyze the given text to get a good understanding of the topics of the post.  Then you will write a section and section title for the given keyword.  You will write a 3-8 paragraph section on the keywords topic using data you know and data in the given blog post. The section must be written in properly formatted html, using <p>, <b>, <ul>, etc when you see fit.   The section title must begin with the given keyword and use related keywords and be under 60 chars long. The title must be written without any html.  Use best practices  for SEO.  You will return a JSON object containing the title, section & a keyword seo optimized alt tag description for the sections image.  There should be no html for the alt tag but it should contain as many keywords as possible and be under 120 characters. The returned JSON object should be like: { title: some keyword optimized title, section: <p>my section content</p>, altTagDescription: keyword optimized alt tag desc of image}.'
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": json.dumps({'keyword': keyword, 'text': self.cleaned_text})}
                ]
            )

            res = json.loads(response.choices[0].message.content)
            
            title = res['title']
            section = res['section']

            sec = '<section><h2>' + title + '</h2>' + section + '</section>'
            p += sec

        return p
        
    
    def get_meta(self):
        title = self.soup.title.string
        # if description is present, get its inner text
        x = self.soup.select('meta[name="description"]')
        # if x is not empty, get the content
        if x:
            description = x[0].attrs["content"]
        else:
            description = ''
            
        # get the keywords
        x = self.soup.select('meta[name="keywords"]')
        # if x is not empty, get the content
        if x:
            keywords = x[0].attrs["content"]
        else:
            keywords = ''
            
        prompt = self.company_info + 'You will receive data for a blog post the company has written.  Using the provided data, you will perfect the title, seo meta description, seo meta keywords.  You will analyze the current posts title: ' + title + ', description: ' + description + ', keywords: ' + keywords + '. And you will also use the new PRIMARY KEYWORD that we just made a few minutes ago: ' + self.primary_keyword + ', as well as the supporting keywords we have made: ' + ','.join(self.supporting_keywords) + ' in order to create the best possible title, seo meta description, seo meta keywords.  You will return a json object containing the title, seo_description, seo_keywords. The json object will look like: {title: title, seo_description: my seo_description, seo_keywords: [keyword1, keyword2, keyword3]}.  You will use the data I provide to calculate the best possible single answer for each.'
    
    def fix_html(self, html, errors):
        print('fix html')
        print(errors)
        prompt = 'You will receive a json object containing errors about an html fragment and the html that needs to be fixed.  you will fix the html fragment and return the fixed html fragment.  You will return me a json object with the fixed html.  The json object will look like: {html: "<section><h2>my title</h2><p>my paragraph</p></section>"}'
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": prompt },
                {"role": "user", "content": json.dumps({'html': html, 'errors': errors})}
            ]
        )
        
        import pdb; pdb.set_trace()
         # convert to json
        
        # get the response:
        res = response.choices[0].message.content
        
       
        
        # get the html
        html = res['html']
        print('fixed html')
        print(html)
        return html
        
    def create_slug(self, data):
        print('create slug')
        prompt = self.company_info + 'You will receive a title for a blog post.  You will create a slug for the post.  The slug must be under 7-10 words long.  The slug must use the primary keyword and 1-2 supporting keywords. No special chars other than the dashes between words. You will return a json object containing the slug. The json object will look like: {slug: my slug}.'
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "user", "content": prompt },
            ]
        )

        res = response.choices[0].message.content
        
        return json.loads(res)['slug']
    
    def rephrase(self, url):
        data = {}
        # GET THE HTML FROM THE URL
        html = requests.get(url)

        # html remove \n
        html = html.text.replace('\n', '')
        html = html.replace('<br>', '')
        html = html.replace('<br/>', '')

        # create beautilful soup object
        self.soup = BeautifulSoup(html, 'html.parser')
        
        title = self.soup.title.string
        description = self.soup.find('meta', attrs={'name': 'description'})
        description = description['content'] if description else ''
        
        tags = self.soup.select('.tags a')
        
        # get the inner text of the a tags
        tagStrings = [tag.get_text().strip() for tag in tags]  # Strip leading/trailing whitespace
        tags = []

        for tag_string in tagStrings:
            normalized_name = tag_string.lower()  # Convert to lowercase or other normalization
            slug = slugify(normalized_name)
            tag, created = Tag.objects.get_or_create(name=normalized_name, slug=slug)
            tags.append(tag)
        
        # get the html element with a class of article-content
        article_content = self.soup.select('.article-content')
        
        # get the children of the article-content element
        chunks = article_content[0].contents



        info = self.create_info(self.soup)
        data['title'] = info['title']
        data['description'] = info['description']
        data['keywords'] = info['keywords']
        
        post_content = ''
        chunk_count = 1
        for chunk in chunks:
            # get the element tag name
            # Check if chunk is a Tag object and get its tag name
            tag_name = chunk.name if chunk and hasattr(chunk, 'name') else None
            print(tag_name)
            # if the chunk is an image, figure, iframe, video, table, or code block, add it directly to the post
            if tag_name in ['img', 'figure', 'iframe', 'video', 'table', 'pre']:
                post_content += str(chunk)
                continue

            print(')))))))))))))))))))))))))))))))))))))))))))))))))))))))')
                
            print('rephrase chunk' + str(chunk_count) + ' of ' + str(len(chunks)))
                
            prompt = "You will receive a large string of html for a blog post from my web development blog.  You will rewrite & rephrase the inner text of all the html tags of the html string you receive so that it is totally unique. You will return the same amount of html that you are given. You will return a json object containing the html. Please make sure to close all html tags.   If any invalid html is given to you, please fix it and return always properly formatted html. The json object will look like: {html: '<section><h2>my title</h2><p>my paragraph</p></section>'}"
                
            # CALL OPENAI TO REWRITE THE HTML
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=[
                    {"role": "system", "content": prompt },
                    {"role": "user", "content": str(chunk)}
                ],
                response_format={ "type": "json_object" },
            )
            
            # GET THE RESPONSE
            res = response.choices[0].message.content
            
            # parse the response
            res = json.loads(res)
            
            post_content += res['html']
            chunk_count += 1

    #     print(')))))))))))))))))))))))))))))))))))))))))))))))))))))))')
        print('rephrase complete')

    #     print(')))))))))))))))))))))))))))))))))))))))))))))))))))))))')
        
    #     # make beautiful soup object
        data['content'] = post_content
        
        slug = slugify(data['title'])
        
        post = BlogPost.objects.create(title=data['title'], content=data['content'], slug=slug, description=data['description'], keywords=data['keywords'])

        
        # add tags
        for tag in tags:
            post.tags.add(tag)
        
        # save the post
        if post.save():
            print('post saved')
            
            return True
        
        return False
    #     # data['featured_image'] = self.create_image(data)
        
    #     # get random post type
    #     post_type = PostType.objects.order_by('?').first()
        
    #     # get random categories 3
    #     categories = Category.objects.order_by('?')[:3]
        
    #     # get random tags 3
    #     tags = Tag.objects.order_by('?')[:3]
        
    #     post = Post.objects.create(
    #         title=data['title'],
    #         subtitle=data['subtitle'],
    #         excerpt=data['excerpt'],
    #         headline=data['headline'],
    #         shadowText=data['shadowText'],
    #         seo_keywords=data['seo_keywords'],
    #         content=data['content'],
    #         seo_title=data['title'],
    #         seo_description=data['excerpt'],
    #         post_status='published',
    #     )
        
    #     # create featured image
    #     featured_image, featured_image_alt = self.create_featured_image(data)
        
    #     post.image_alt_text = featured_image_alt
    #     post.featured_image.save(slugify(data['title']) + '.png', ContentFile(featured_image), save=True)
    #         # add post type
    #     post.post_type = post_type
        
    #     # add categories
    #     for category in categories:
    #         post.categories.add(category)
            
    #     # add tags
    #     for tag in tags:
    #         post.tags.add(tag)
            
    #     if post.save():
    #         print('post saved')
            
            
            
    #     return data
    
    # return False
    
    def removeAttrs(self, soup):
        # I PERSONALLY LIKE TO REMOVE ALL HTML ATTRS TO MAKE THE TOKEN SIE AS SMALL AS POSSIBLE
        for tag in soup.find_all(True):
            tag.attrs = None
        return soup
    
        # Your initialization code

    def recursive_add_children(self, children):
        newlist = []

        # loop over children and print the length
        for index, child in enumerate(children):
            # convert child to string
            child_string = str(child)

            if self.valid_text_size(child_string):
                new_child = child_string + str(children[index + 1]) if index + 1 < len(children) else ""

                # check if the child string plus the next child string is a valid size
                if self.valid_text_size(new_child):
                    child_string = new_child
                    # remove the child from the parent
                    newlist.append(child_string)

                    # Add more logic to obtain additional children or modify the existing ones
                    additional_children = ...

                    # Call the function recursively
                    recursive_result = self.recursive_add_children(additional_children)

                    # Extend the newlist with the result of the recursive call
                    newlist.extend(recursive_result)

        print(len(newlist))
        return newlist

    
    def prepare_html(self):
         # remove all new lines

        # get parent element
        # remove all html attrs
            
        # remove all new lines
        [s.extract() for s in self.soup('br')]
        # remove all script tags
        [s.extract() for s in self.soup('script')]
        
        # remove all noscript tags
        [s.extract() for s in self.soup('noscript')]
        
        # remove all iframe tags
        [s.extract() for s in self.soup('iframe')]
        
        # remove all style tags
        [s.extract() for s in self.soup('style')]
        
        # remove all meta tags
        [s.extract() for s in self.soup('meta')]
        
        # remove all image tags
        [s.extract() for s in self.soup('img')]
        
        # remove all video tags
        [s.extract() for s in self.soup('video')]
        
        # YOU DONT HAVE TO DO THE ABOVE BUT MY POSTS AREVERY LONGANDI DO NOT NEED THOSE ELEMENTS IN MY HTML
        parent = self.soup.select('.post-content')
        parent = parent[0]

        self.removeAttrs(parent)

        # get the first child AND LOOP OVER EVERY CHILD AND MAKE SURE THAT IT IS NOT TOO LONG
        # IF IT IS, I SKIP IT AND MOVE ON TO THE NEXT CHILD

        # get the html element ith the class of .content-small


        children = parent.contents

        print(len(children))

        children = self.consolidate_items(children)
        
        print(len(children))
        
        return children
    
    def consolidate_items(self, items):
        consolidated_list = []

        index = 0
        current_item = str(items[index])

        while index < len(items) - 1:
            next_item = str(items[index + 1])
            combined_item = current_item + next_item

            if self.valid_text_size(str(combined_item)):
                current_item = combined_item
            else:
                consolidated_list.append(current_item)
                current_item = str(items[index + 1])

            index += 1

        consolidated_list.append(current_item)

        print(len(consolidated_list))
        return consolidated_list
    
    def create_info(self, soup):
        print('create info')
         # get title and description
        title = soup.title.string
        
        # if description is present, get its inner text
        x = soup.select('meta[name="description"]')
        # if x is not empty, get the content
        if x:
            description = x[0].attrs["content"]
            
        # get 
        s = {
            'title': title,
            'description': description,
        }

        # stringify info
        s = json.dumps(s)
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": "you will get a title, description and list of seo meta keywords for a blog post.the keywords will be returned as a string with comma seperated values.  You will rewrite the title & description so it is unique, but still captures the same meaning.  You will return a json object containing the title, keywords & description. The json object will look like: {title: my title, description: my description, keywords: kw1,kw2,kw3}." },
                {"role": "user", "content": s}
            ]
        )

        tojson = response.choices[0].message.content
        
        # convert to json

        tojson = json.loads(tojson)
        return tojson
    
    def create_featured_image(self, post):
        print('create featured image')
        title = post['title']
        subtitle = post['subtitle']
        excerpt = post['excerpt']
        keywords = post['seo_keywords']
        # Define your prompt for DALL·E
        prompt = 'My company is a Dropshipping product importer and management app for Shopify stores.  I have a blog post that needs a beautiful eye catching featured image.  The blog post is based on the following details.  The title: ' + title + ' and the subtitle: ' + subtitle + ' and the excerpt: ' + excerpt + ' and the seo keywords: ' + str(keywords) + '.  Please create a beautiful featured image for this blog post that makes sense for a post with the previously mentioned info.  The image should be landscape, hi-res, unique & eye catching.  The image should be 1920px1080px.  The image should be a png file.  The image should be under 1mb.  The image should be unique and not used anywhere else on the internet.  The image should be related to the topic of the blog post.  The image should be a beautiful image that will make people want to read the blog post.  The image should be a beautiful image that will make people want to read the blog post.  The image should use gradients & colors to make it stand out.'
        
        

        # Call the OpenAI API to generate the image
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1792x1024",
            n=1  # Specify the number of images to generate
        )

        img_url = response.data[0].url

        # Download the image using requests
        image_response = requests.get(img_url)
        
        featured_image = image_response.content
        
        # prompt to write a alt tag description for the image
        prompt = self.company_info + 'You must write an seo focused alt tag description for the featured image of the post with the details: title: ' + title + ' and subtitle: ' + subtitle + ' and excerpt: ' + excerpt + ' and seo keywords: ' + str(keywords) + '.  The alt tag description must be under 120 characters. The alt tag description must use the primary kew word and use 3-5 supporting keywords.  You will return a json object containing the alt_tag_description. The json object will look like: {alt_tag_description: my alt_tag_description}.'
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={"type": "json_object"},
            messages=[
                {"role": "user", "content": prompt },
            ]
        )
        
        res = json.loads(response.choices[0].message.content)
        
        featured_image_alt = res['alt_tag_description']
        
        
        return featured_image, featured_image_alt
    
    
    def write_post(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        
        # title tag
        title = soup.title.string
        
        # meta description tag
        description = soup.find('meta', attrs={'name': 'description'})
        import pdb; pdb.set_trace()
        p = 'this is the title: ' + title + ' and this is the description: ' + description['content']
        t = self.create_title(p)
        import pdb; pdb.set_trace()
        
 
    def uniquify(self, url):
        print('uniquify')
        
        if url is None:
            return False
        #get the html
        html = requests.get(url)
        
        # create beautiful soup object
        self.soup = BeautifulSoup(html.text, 'html.parser')
        
        #get the title
        title = self.soup.title.string
        
        # if description is present, get its inner text
        x = self.soup.select('meta[name="description"]')
        # if x is not empty, get the content
        if x:
            description = x[0].attrs["content"]
        else:
            description = ''
            
        # get the keywords
        x = self.soup.select('meta[name="keywords"]')
        # if x is not empty, get the content
        if x:
            keywords = x[0].attrs["content"]
        else:
            keywords = ''
        
        
        # get the 2nd html element with a class of .content-small
        post_html = self.soup.select('.content-small')[1]
        
        # remove all script tags
        [s.extract() for s in post_html('script')]
        
        # remove all style tags
        [s.extract() for s in post_html('style')]
        
        # remove all meta tags
        [s.extract() for s in post_html('meta')]
        
        # remove all noscript tags
        [s.extract() for s in post_html('noscript')]
        
        # remove all image tags
        [s.extract() for s in post_html('img')]
        
        #remove all attributes the post_html
        post_html = self.removeAttrs(post_html)
        idx = 0
        # split post_html into chunks of 5000 characters
        chunks = split_string_with_limit(str(post_html), self.max_tokens/2, self.token_encoding)
        post = ''
        # loop over chunks and send to openai
        for chunk in chunks:
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": self.company_info + ". You ill receive a part of a long html blog post.  You will rewrite and reword the htmls inner text to make it unique. You will return a json object like {html: '<p>my new html</p>'}" },

                    {"role": "user", "content": str(chunk)}
                ]
            )
            res = response.choices[0].message.content
            res = json.loads(res)
            post += res['html']

            print(idx)
            print(len(chunks))
            idx += 1

        # prompt to send to openai describing how to use the current post title, description, keywords to create a new title, description, keywords that use the same primary keyword, and supporting keywords but are unique and different from the current title, description, keywords
        prompt = self.company_info + 'You will receive a title, description, keywords for a blog post.  You will use the title, description, keywords to create a new title, description, keywords that use the same primary keyword, and supporting keywords but are unique and different from the current title, description, keywords. The title should be less than 60 characters & the first word must be the posts primary seo keyword.  The description should be less than 120 characters & must use as many keywords as possible. You will also generate a list of 50 keywords & phrases for the meta keywords tag. A subtitle is required and must use the main keyword and 2 other supporting keywords and will be less than 60 words. A short header title, a small intro title above the primary title is needed and is meant to be a short lead in phrase to the main title.  A Shadoe Text title i a 2-5 word alternative phrase for the overall topic of the post.  You will return a json object containing the title, excerpt, seo keywords, subtitle, headline, shadowText.  The json object will look like: {title: my title, excerpt: my excerpt, seo_keywords: [keyword1, keyword2, keyword3], subtitle: my subtitle, headline: my header title, shadowText: my shadow text title}.'
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": prompt },
                {"role": "user", "content": json.dumps({'title': title, 'description': description, 'keywords': keywords}) }
            ]
        )
        
        res = response.choices[0].message.content
        
        # convert to json
        res = json.loads(res)
        
        new_post = {
            'title': res['title'],
            'excerpt': res['excerpt'],
            'subtitle': res['subtitle'],
            'headline': res['headline'],
            'shadowText': res['shadowText'],
            'seo_keywords': res['seo_keywords'],
            'content': post,
            'featured_image': self.create_featured_image(res)
        }
        
        return new_post
    
        
    

    def process_audio(self, audio_file):
        am = AudioManager()
        transcription = am.process_audio(audio_file)
        
        return transcription
     
     
    def write_all(self):
        topics = BlogTopic.objects.filter(used=False)
        
        for topic in topics:
            url = topic.url
            made_post = self.rephrase(url)
            
            if made_post:
                # delete the topic
                topic.delete()