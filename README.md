# Guide d'introduction à Wagtail

## Initialisation du projet

Créez un dossier dans le repertoire de votre choix.

```bash
mkdir jobboard
cd jobboard
```

### Configurez l'environnement virtuel

Création de l'environnement

```bash
python -m venv env
```

Activation de l'environnement

```bash
source env/bin/activate
```

### Installation wagtail

```bash
pip install wagtail
```

Vérification de l'installation (facultatif)

```bash
pip list
```

**Création du projet**
Assurez-vous d'être dans le repertoire `jobboard` créé précédemment et n'oubliez pas de mettre le **.** (point).

```bash
wagtail start jobboard .
```

Afin d'assurer la compatibilité des dépedances, Wagtail nous crée un fichier `requirements.txt`. Il est important de les installer afin que le projet lance convenablement.

```bash
pip install -r requirements.txt
```

**Création de la base de données**

```bash
python manage.py migrate
```

**Création du compte admin**

```bash
python manage.py createsuperuser
```

Cette commande permet de créer un nom d'utilisateur et un mot de passe pour connecter dans l'interface admin de Wagtail.

**Lancement du serveur de développement**

```bash
python manage.py runserver
```

Maintenant visitez <http://127.0.0.1:8000>, si vous voyez cette page, tout va bien et on est prêts pour la suite.

Pour plus d'infos, [consultez la documentation](https://docs.wagtail.org/en/stable/getting_started/tutorial.html).

![alt text](https://github.com/Thevenel/wagtail_resources/blob/main/assets/img/welcome-page-wagtail.png?raw=true)

## Le Job App

Dans Wagtail comme Django, chaque application est indépendante et réutilisable. Une fois créée, une application peut être partagée afin de l'utiliser dans d'autres projets. Pour créer une app dans Wagtail, le mécanisme est le même que celui de Django.

```bash
python manage.py startapp job
```

C'est l'application principale, on y trouve tout ce qui est rélatif à la publication d'un `job`. On doit l'ajouter dans la liste des applications installées dans le projet après sa création.
`jobboard/settings/base.py`.

```python
INSTALLED_APPS = [
    "job", # <- notre Job app.
    "home",
    "search",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    #... autres
]
```

### Une approche différente du pattern MVT

Généralement, Django est un Framework **MVT** (Model, View, Template). Le `Model` définit la structure de la base de données, les logiques de l'application se trouvent dans la `View` et le `Template` permet d'afficher le contenu HTML.

Dans Wagtail, on ne travaillle pas avec `View` et la majeur partie du travail se fait dans le `Model`. De plus, il est important de comprendre les différents concepts de Wagtail afin de faciliter le processus de développement.

#### Quelques concepts clés

**Pages :** Les pages sont la base fondamentale du CMS Wagtail. Chaque Page est un model de Python (Django). Elle est héritée du modèle `Page`. Cette classe contient une multitude de méthodes permettant d'adapter le comportement de la page à son utilisation. La plus utilisée est probablement `get_context`.

**StreamField :** C'est un champ puissant qui permet de créer des pages de contenus structurés en utilisant des `blocks`.

**Blocks :** Ce sont des contenus réutilisables à l'intérieur d'un champ `StreamField`. Wagtail contient plusieurs `blocks` intégrés, mais vous pouvez créer des `blocks` personnalisés.

**Images, Documents, Snippets :** Ce sont d'autres types de contenus qu'on peut utiliser à l'intérieur des `pages` et des `blocks`.

**Templates :** Ce sont des contenus rendus en HTML en utilisant des Templates Django.

**Interface Admin :** C'est un interface intuitif permettant de gérer des contenus, utilisateurs et les configurations de site.

#### La page index des jobs

```python
# Django imports
from django.db import models

# Wagtail imports
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class JobListing(Page):
    intro = RichTextField()
    
    # add to the admin interface
    content_panels = Page.content_panels + [
        FieldPanel("intro")
    ]
```

Le modèle `JobListing` est hérité de `Page` du *package* `wagtail.models`. Le champs `RichTextField` importé du *package*, permet d'avoir le format enrichi qu'on trouve le plus souvent dans les logiciels de traitement de texte.

L'attribut `content_panels` permet d'éditer les contenus dans l'interface Admin. C'est une liste pouvant recevoir plusieurs autres champs. Dans ce cas, on utilise `FieldPanel` de `wagtail.admin.panels`.

**Migrations**

```bash
# Créer les migrations
python manage.py makemigrations

# Exécuter les migrations
python manage.py migrate
```

Maintenant, on peut commencer à créer des pages à partir de admin > Pages > add child page. Même après avoir ajouté du contenu à la page, elle n'est visible qu'après la création du `Template`.

**Templates**
Wagtail requiert que tous ses templates soint la version `snake_case` du nom du modèle. Par exemple, `JobListing` devient, `job_listing`. De plus, il va les chercher dans le repertoire `app_name/templates/app_name`. On va maintenant le `Template` dans `job/templates/job/job_listing.html`

```html
{% extends "base.html" %}
{% load wagtailcore_tags %}

{% block content %}
    {{self.title}}
    <p> {{ self.intro|richtext }} </p>

{% endblock content %}
```

On va utiliser cette page pour afficher les differents jobs publiés.

#### La page Job

```python
class JobPage(Page):
    date = models.DateField(verbose_name="Published Date", default=timezone.now)
    location = models.CharField(max_length=100)
    short_description = models.CharField(max_length=200, help_text="Max 200 characters")
    thumbnail = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
        help_text="Choose a image for your cover"
    )
    salary = models.IntegerField(verbose_name="A salary approximation")
    company = models.CharField(max_length=200)
    
    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("location"),
        FieldPanel("short_description"),
        FieldPanel("thumbnail"),
        FieldPanel("salary"),
        FieldPanel("company")
    ]
```

Dans ce modèle, le champs `thumbnail` est plus important, car Wagtail traite les images différemment. L'image est une clé étrangère de la classe `wagtailimages.Image`.

**Migrations**

```bash
# Créer les migrations
python manage.py makemigrations

# Exécuter les migrations
python manage.py migrate
```

On peut maintenant utiliser cette classe dans l'interface Admin. Cette page doit être une page enfant de la page `Job Listing`.

**Templates**
On peut créer le `Template` dans `job/templates/job/job_page.html`

**StreamField en action**
Les `StreamField` permettent d'avoir plus de flexibilité au niveau de la manipulation des contenus. Il existes différents types de [blocks](https://docs.wagtail.org/en/stable/reference/streamfield/blocks.html) adaptés à chaque type de contenu. On va utiliser des `StreamField` pour le corps d'une publication.

```python

# Wagtail imports updated (StreamField, blocks)
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail import blocks


class JobPage(Page):
    date = models.DateField("Published Date", default=timezone.now)
    location = models.CharField(max_length=100)
    short_description = models.CharField(max_length=200, help_text="Max 200 characters")
    thumbnail = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
        help_text="Choose a image for your cover"
    )
    salary = models.IntegerField(verbose_name="A salary approximation")
    company = models.CharField(max_length=200)
    # update
    content = StreamField(
        [
            ('heading', blocks.CharBlock(form_classname='full title', template='blocks/heading.html')),
            ('paragraph', blocks.RichTextBlock(template='blocks/paragraph.html')),
            ('blockquote', blocks.BlockQuoteBlock(template='blocks/blockquote.html')),
            ('list', blocks.ListBlock(blocks.CharBlock(), template='blocks/list.html')),
            ('html', blocks.RawHTMLBlock(template='blocks/html.html')),
            ('image', ImageChooserBlock())
        ],
        null=True, 
        blank=True
        
    )
    
    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("location"),
        FieldPanel("short_description"),
        FieldPanel("thumbnail"),
        FieldPanel("salary"),
        FieldPanel("company"),
        FieldPanel("content") # update
    ]
```

**Migrations**

```bash
# Créer les migrations
python manage.py makemigrations

# Exécuter les migrations
python manage.py migrate
```

A ce niveau, notre `Template` est géré différemment. Le `StreamField` prend une liste de couple en entrée, (`nom`, `type_de_block`) . Pour récupérer le `block` en question,  nn itère à travers les blocks du champs `content` et on compare le type de `block`.

```html
{% extends "base.html" %} 
{% load wagtailcore_tags wagtailimages_tags %} 

{% block content %}

    {{self.title}}
    {{self.salary}}

    {% for block in self.content %}
        {% if block.block_type == 'heading' %}
            <h2>{{block.value}}</h2>
        {% elif block.block_type == 'paragraph' %}
            <p>{{block.value}}</p>
        {% endif %}
    {% endfor %}

{% endblock content %}
```

Ça fonctionne, mais le code devient de plus en plus difficile à lire. C'est pourquoi il est récommandé de créer un template dédier à chaque `block`. On crée un repertoire `blocks` dans `templates`. Et Wagtail recupérer chaque block à cause du template qu'on a défini dans le modèle.

Le `Template` `job_page.html`  devient.

```html
  {% for block in self.content %}
        {{block}}
    {% endfor %}
```

`heading.html`

```html
<h3>{{ value }}</h3>
```

`paragraph.html`

```html
{% load wagtailcore_tags %}

<p>{{ value|richtext }}</p>
```

`blockquote.html`

```html
<blockquote>
    <p> {{ value }}</p>
</blockquote>
```

### Gestion de contexte

On va revenir sur la page index des publications. Wagtail est organisé en forme d'un arbre, d'où l'intéret de bien choisir la page parente au moment de la création d'une page. Lorsqu'on souhaite utiliser les donnée d'une page dans une autre, on doit modifier la méthode `get_context`.

On va dans la classe `JobListing` et on modifie la méthode `get_context`.

```python
def get_context(self, request):
    # Update context to include all live JobPage instances
    context = super().get_context(request)
    context['jobs'] = JobPage.objects.live()  # Fetch all published JobPage objects
    return context
```

Après avoir modifié la méthode `get_context`, on peut accéder les objets dans le `Template` avec la variable `jobs`.
 [job_listing.html](https://github.com/Thevenel/wagtail_resources/blob/main/snippets/job_listing.html)

```html
   {% for job in jobs %}
        {{job.title}}
        {{job.thumbnail}}
    {% endfor %}
```

## Style

Il n'est pas amusant de travailler avec un CMS sans style. Ajoutons un peu de style. Pour la simplicité, nous allons utiliser `Bootstrap`. Lors de la création du projet, Wagtail crée un dossier `static` dans lequel se trouve un fichier avec ayant le même nom que le projet. Nous allons ajouter notre fichier `bootstrap.min.css` dans le dossier `css`. Ensuite, ajouter le lien dans le fichier `base.html`.

**Job Listing**

**Home Page**

Le model de la page d'accueil est simple à implementer, elle est similaire à la page `job`. Mais on peut aussi ajouter un `block_counts` qui définit le nombre de block maximal ou maximal que peut avoir le `StreamField`. Pour le lien CTA, on procède la même façon que l'image. Cette fois on crée la clé étrangère vers `wagtailcore.Page`, ce qui permet de rédiriger vers une autre page. Enfin, la méthode `get_context` nous permet de récupérer les trois derniers `jobs` publiés sur la page d'accueil.

Dans ce `model`, on utilise `MultiFieldPanel` pour regrouper les champs dans l'interface utilisateur.

```python
class HomePage(Page):
    image = models.ForeignKey(
        "wagtailimages.Image",
        null = True,
        blank = True,
        on_delete = models.SET_NULL,
        related_name = "+",
        help_text = "Homepage image"
    )
    hero_text = models.CharField(max_length=255, help_text="Make the home stand out")
    hero_cta = models.CharField(
        verbose_name="Hero CTA",
        max_length=255,
        help_text="Add a CTA text`", 
        blank=True, 
        null=True
    )
    hero_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null = True,
        blank = True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Hero CTA link",
        help_text="Choose a page to link to for the CTA"
    )
    feature_section_title = models.CharField(max_length=100, null=True, blank=True)
    features = StreamField(
        [
            ('feature_icon', ImageChooserBlock(required=False)),
            ('feature_title', blocks.CharBlock(required=True)),
            ('feature_desc', blocks.CharBlock(required=True))
        ],

        null = True,
        blank = True
    )
    def get_context(self, request):
        context = super().get_context(request)
        context['jobs'] = JobPage.objects.live().order_by('-first_published_at')
        return context

    content_panels = Page.content_panels + [
        MultiFieldPanel (
            [
                FieldPanel("image"),
                FieldPanel("hero_text"),
                MultiFieldPanel (
                    [
                        FieldPanel("hero_cta"),
                        FieldPanel("hero_cta_link")
                    ]
                ) 
            ],
            heading = "Hero section"
        ),
        FieldPanel("feature_section_title"),
        FieldPanel("features")
    ]
```

Le template

## La barre de navigation

Pour créer la barre de navigation, il est nécessaire de comprendre la strucure d'un arbre. En effet, la page d'accueil est la racine et toutes autres pages y sont rattachées.

On va commencer par créer un fichier qu'on appelera `templatetags/navigation_tags.py` dans le repertoire `home`. Ce fichier va nous permet de récupérer la racine de notre site à l'aide de la classe `Site`, pour plus d'infos consulter la documentation ici.

```python
from django import template
from wagtail.models import Site


register = template.Library()
@register.simple_tag(takes_context=True)
def get_site_root(context):
    return Site.find_for_request(context["request"]).root_page
```

On utilise la class `Library` du package `template` de Django récupérer le context et en créer une annotation. Pour finir, la méthode `get_site_root` récupère la racine à partir de la requête. C'est bien cette méthode qu'on va utiliser dans notre `template`.

On peut maintenant passer à l'étape suivante qui est de créer un `jobboard/templates/includes/header.html`. Ce fichier utilisera notre méthode pour créer la navigation.

```html
    <!-- includes/header.html -->
    {% load wagtailcore_tags navigation_tags %}    
    
        {% get_site_root as site_root %}
        <ul>
            <li>
                <a href="{% pageurl site_root %}">Home</a>
            </li>
            {% for menuitem in site_root.get_children.live.in_menu %}
                <li>
                    <a href="{% pageurl menuitem %}">{{ menuitem.title }}</a>
                </li>
            {% endfor %}
        </ul>
```

Dans cette portion de code, on crée un alias pour notre méthode `get_site_root` et le définit comme le lien vers lequel on se rédirige en cliquant sur `Home`. Ensuite, on crée une boucle pour parcourir les pages et récupérer celles qui sont publiques et font partie du menu. On peut maintenant ajouter d'autres pages dans le menu en cliquant dans l'onglet `promote` et cocher la case `show in menus`.


## Le pied de page

À ce point, l'implementation du pied de page nous parraitra plus simple car on comprend mieux le principe. Toutefois, il existe deux types d'implementation. La première se fait en créant des paramètres de navigation et la seconde à l'aide de `snippets`. Pour faire simple, on va utiliser la méthode, vous pouvez voir la seconde implementation [ici](https://docs.wagtail.org/en/latest/tutorial/create_footer_for_all_pages.html#create-editable-footer-text-with-wagtail-snippets).

> Il est recommandé de créer une app `base` dans laquelle se trouve tous fichiers mais, on l'ajouter dans `home/models.py` pour simplifier la tache.

```python
# new imports
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    register_setting
)

@register_setting
class NavigationSettings(BaseGenericSetting):
    linkedin_url = models.URLField(verbose_name="Linkedin URL", blank=True)
    github_url = models.URLField(verbose_name="GitHub URL", blank=True)
    mastodon_url = models.URLField(verbose_name="Mastodon URL", blank=True)
    
    panels = [
        MultiFieldPanel(
            [
                FieldPanel("linkedin_url"),
                FieldPanel("github_url"),
                FieldPanel("mastodon_url")
            ],
            "Social settings"
        )
    ]
```

> N'oubliez pas les migrations

Les paramètres généraux communs entre toutes les pages se trouvent dans le module `wagtail.contrib.settings`. On doit enregistrer ce module dans la liste des `INSTALLED_APPS`.

```python
INSTALLED_APPS = [
    # ... cette ligne permet d'installer wagtail.contrib.settings
    "wagtail.contrib.settings",
]
```

La prochaine étape consiste à enregistrer les paramètres dans le processeur de context. Ce dernier rend les paramètres accessibles dans les `templates`. Pour y enregistrer les paramètres, on ajoute cette ligne dans `jobboard/settings/base.py`: `"wagtail.contrib.settings.context_processors.settings",`

```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",

                # Add this to register the _settings_ context processor:
                "wagtail.contrib.settings.context_processors.settings",
            ],
        },
    },
]
```

