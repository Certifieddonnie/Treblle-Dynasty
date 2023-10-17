<div align="center">
  <img src="https://treblle-github.s3.amazonaws.com/header.png"/>
</div>
<div align="center">

# Treblle

<a href="https://docs.treblle.com/en/integrations" target="_blank">Integrations</a>
<span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
<a href="http://treblle.com/" target="_blank">Website</a>
<span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
<a href="https://docs.treblle.com" target="_blank">Docs</a>
<span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
<a href="https://blog.treblle.com" target="_blank">Blog</a>
<span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
<a href="https://twitter.com/treblleapi" target="_blank">Twitter</a>
<span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
<a href="https://treblle.com/chat" target="_blank">Discord</a>
<br />

  <hr />
</div>

### FastAPI for Treblle
![image](https://github.com/Certifieddonnie/treblle-dynasty/assets/98459984/0ee4b7a4-f9f2-44ff-b6ef-ef5df2ffda18)



Treblle is a lightweight SDK that helps Engineering and Product teams build, ship & maintain REST based APIs faster.

## Features

<div align="center">
  <br />
  <img src="https://treblle-github.s3.amazonaws.com/features.png"/>
  <br />
  <br />
</div>

- [API Monitoring & Observability](https://www.treblle.com/features/api-monitoring-observability)
- [Auto-generated API Docs](https://www.treblle.com/features/auto-generated-api-docs)
- [API analytics](https://www.treblle.com/features/api-analytics)
- [Treblle API Score](https://www.treblle.com/features/api-quality-score)
- [API Lifecycle Collaboration](https://www.treblle.com/features/api-lifecycle)
- [Native Treblle Apps](https://www.treblle.com/features/native-apps)


## How Treblle Works
Once you’ve integrated a Treblle SDK in your codebase, this SDK will send requests and response data to your Treblle Dashboard.

In your Treblle Dashboard you get to see real-time requests to your API, auto-generated API docs, API analytics like how fast the response was for an endpoint, the load size of the response, etc.

Treblle also uses the requests sent to your Dashboard to calculate your API score which is a quality score that’s calculated based on the performance, quality, and security best practices for your API.

> Visit [https://docs.treblle.com](http://docs.treblle.com) for the complete documentation.

## Security

### Masking fields
Masking fields ensure certain sensitive data are removed before being sent to Treblle.

To make sure masking is done before any data leaves your server [we built it into all our SDKs](https://docs.treblle.com/en/security/masked-fields#fields-masked-by-default).

This means data masking is super fast and happens on a programming level before the API request is sent to Treblle. You can [customize](https://docs.treblle.com/en/security/masked-fields#custom-masked-fields) exactly which fields are masked when you’re integrating the SDK.

> Visit the [Masked fields](https://docs.treblle.com/en/security/masked-fields) section of the [docs](https://docs.sailscasts.com) for the complete documentation.


## Get Started

1. Sign in to [Treblle](https://app.treblle.com).
2. [Create a Treblle project](https://docs.treblle.com/en/dashboard/projects#creating-a-project).
3. [Setup the SDK](#install-the-SDK) for your platform.

### Install the SDK
You can install Treblle for FastAPI, by following the commands below.
```bash
pip install trenasty
```
### Configuration
Once you have installed the Treblle SDK for FastAPI, you will need to configure it in your app. This can be done by creating a **.env** file and adding the following variables:

```python
TREBLLE_API_KEY = ''
TREBLLE_PROJECT_ID = ''
TIME_ZONE = ''
TREBLLE_SENSITIVE_KEYS = []
#[id, email]

```
- **TREBLLE_API_KEY**: Your Treblle API key, which you can obtain by signing in to your Treblle account.
- **TREBLLE_PROJECT_ID**: Your Treblle project ID.
- **TIME_ZONE**: The time zone setting for your application.
- **TREBLLE_SENSITIVE_KEYS**: A list of keys that should be masked in your logs, such as **id, access_token, email, or any other sensitive information you want to keep secure.**
  
`Once you have created the .env file, you can initialize the Treblle middleware in your FastAPI app`

### Initialization

This is the step to initialize the middleware in your FastAPI app.

**Importing FastAPI in Treblle Middleware**
```python
from fastapi import FastAPI
from trenasty.middleware.treblle import TreblleMiddleware
```

**Instantiating the App and the Middleware**
```python
app = FastAPI()

app.middleware("http")(TreblleMiddleware(app))

```

### Authentication and Access 
Authentication in Treblle usually involves securing your API key and project ID. You should never expose these keys directly in your codebase. Instead, store them in environment variables (as shown above) and load them in your application securely.

Access control in Treblle is typically managed through your Treblle account and project settings. You can define who has access to your project within the Treblle dashboard. Be cautious about sharing your API key, and only grant access to trusted team members.

**Treblle supports a variety of authentication and authorization mechanisms. You can choose the one that best suits your needs.**

- **API Keys**
You can use API keys to authenticate users with Treblle. To do this, you will need to generate an API key for each user. You can then add the API key to the Authorization header of each request.

- **OAuth 2.0**
You can also use OAuth 2.0 to authenticate users with Treblle. To do this, you will need to create an OAuth 2.0 client in Treblle. You can then use the client ID and secret to obtain an access token for each user. You can then add the access token to the Authorization header of each request.

- **Custom Authentication**
You can also implement your own authentication mechanism for Treblle. To do this, you will need to create a custom authentication middleware. You can then use the middleware to authenticate users before they can access your app's resources.

###


## Other Available SDKs

Treblle provides [open-source SDKs](https://docs.treblle.com/en/integrations) that let you seamlessly integrate Treblle with your REST-based APIs.

- [`treblle-laravel`](https://github.com/Treblle/treblle-laravel): SDK for Laravel
- [`treblle-php`](https://github.com/Treblle/treblle-php): SDK for PHP
- [`treblle-symfony`](https://github.com/Treblle/treblle-symfony): SDK for Symfony
- [`treblle-lumen`](https://github.com/Treblle/treblle-lumen): SDK for Lumen
- [`treblle-sails`](https://github.com/Treblle/treblle-sails): SDK for Sails
- [`treblle-adonisjs`](https://github.com/Treblle/treblle-adonisjs): SDK for AdonisJS
- [`treblle-fastify`](https://github.com/Treblle/treblle-fastify): SDK for Fastify
- [`treblle-directus`](https://github.com/Treblle/treblle-directus): SDK for Directus
- [`treblle-strapi`](https://github.com/Treblle/treblle-strapi): SDK for Strapi
- [`treblle-express`](https://github.com/Treblle/treblle-express): SDK for Express
- [`treblle-koa`](https://github.com/Treblle/treblle-koa): SDK for Koa
- [`treblle-go`](https://github.com/Treblle/treblle-go): SDK for Go
- [`treblle-ruby`](https://github.com/Treblle/treblle-ruby): SDK for Ruby on Rails
- [`treblle-python`](https://github.com/Treblle/treblle-python): SDK for Python/Django

> See the [docs](https://docs.treblle.com/en/integrations) for more on SDKs and Integrations.

## Other Packages

Besides the SDKs, we also provide helpers and configuration used for SDK
development. If you're thinking about contributing to or creating a SDK, have a look at the resources
below:

- [`treblle-utils`](https://github.com/Treblle/treblle-utils):  A set of helpers and
  utility functions useful for the JavaScript SDKs.
- [`php-utils`](https://github.com/Treblle/php-utils):   A set of helpers and
  utility functions useful for the PHP SDKs.

## Community 💙

First and foremost: **Star and watch this repository** to stay up-to-date.

Also, follow our [Blog](https://blog.treblle.com), and on [Twitter](https://twitter.com/treblleapi).

You can chat with the team and other members on [Discord](https://treblle.com/chat) and follow our tutorials and other video material at [YouTube](https://youtube.com/@treblle).

[![Treblle Discord](https://img.shields.io/badge/Treblle%20Discord-Join%20our%20Discord-F3F5FC?labelColor=7289DA&style=for-the-badge&logo=discord&logoColor=F3F5FC&link=https://treblle.com/chat)](https://treblle.com/chat)

[![Treblle YouTube](https://img.shields.io/badge/Treblle%20YouTube-Subscribe%20on%20YouTube-F3F5FC?labelColor=c4302b&style=for-the-badge&logo=YouTube&logoColor=F3F5FC&link=https://youtube.com/@treblle)](https://youtube.com/@treblle)

[![Treblle on Twitter](https://img.shields.io/badge/Treblle%20on%20Twitter-Follow%20Us-F3F5FC?labelColor=1DA1F2&style=for-the-badge&logo=Twitter&logoColor=F3F5FC&link=https://twitter.com/treblleapi)](https://twitter.com/treblleapi)

### How to contribute

Here are some ways of contributing to making Treblle better:

- **[Try out Treblle](https://docs.treblle.com/en/introduction#getting-started)**, and let us know ways to make Treblle better for you. Let us know here on [Discord](https://treblle.com/chat).
- Join our [Discord](https://treblle.com/chat) and connect with other members to share and learn from.
- Send a pull request to any of our [open source repositories](https://github.com/Treblle) on Github. Check the contribution guide on the repo you want to contribute to for more details about how to contribute. We're looking forward to your contribution!

### Contributors
<!-- Replace link with the link of the SDK contributors-->
<a href="https://github.com/Certifieddonnie/Treblle-Dynasty/graphs/contributors">
  <p align="center">
    <img  src="https://contrib.rocks/image?repo=Certifieddonnie/Treblle-Dynasty" alt="A table of avatars from the project's contributors" />

  </p>
</a>
