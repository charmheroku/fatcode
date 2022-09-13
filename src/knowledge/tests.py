from collections import OrderedDict

from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from src.knowledge import models
from src.profiles.models import FatUser


class TestKnowledge(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        user = FatUser.objects.create(
            username='anton',
            password='V97tn7M4rU',
            email='anton@example.com'
        )
        models.Article.objects.create(
            title='first article',
            text='text of the first article',
            author=user,
            published=True,
        )
        models.Article.objects.create(
            title='second article',
            text='text of the second article',
            author=user,
            published=True,
        )

        models.Tag.objects.create(name='python')
        models.Tag.objects.create(name='django')

        models.Glossary.objects.create(letter="f")

        models.Category.objects.create(name='Python')
        web_cat = models.Category.objects.create(name='Web')
        models.Category.objects.create(name='Django', parent=web_cat)

    def test_article_list(self):
        url = reverse("article-list")
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(len(request.data["results"]), 2)

    def test_article_detail(self):
        article = models.Article.objects.get(title='first article')
        url = reverse("article-detail", kwargs={"id": article.id})
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['title'], 'first article')
        self.assertEqual(request.data['text'], 'text of the first article')

    def test_tag_list(self):
        url = reverse("tag-list")
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(len(request.data), 2)

    def test_category_list(self):
        url = reverse("category-list")
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(len(request.data), 3)

    def test_category_detail(self):
        category = models.Category.objects.get(name='Django')
        category_par = models.Category.objects.get(name='Web')
        url = reverse("category-detail", kwargs={"id": category.id})
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['name'], 'Django')
        self.assertEqual(request.data['parent'], category_par.pk)

    def test_get_glossary_letters(self):
        url = reverse("glossary-letter")
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data[0], OrderedDict([('id', 1), ('letter', 'f')]))
