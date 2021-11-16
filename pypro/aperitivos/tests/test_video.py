import pytest
from django.urls import reverse
from pypro.django_assertions import assert_contains
from pypro.aperitivos.models import Video


@pytest.fixture
def video(client, db):
    v = Video(slug='motivacao', titulo='Video Aperitivo: Motivação', vimeo_id=639324828)
    v.save()
    return v


@pytest.fixture
def resp(client, video):
    return client.get(reverse('aperitivos:video', args=(video.slug, )))


@pytest.fixture
def resp_video_nao_encontrado(client, video):
    return client.get(reverse('aperitivos:video', args=(video.slug + 'video_nao_existente', )))


def test_status_code(resp):
    assert resp.status_code == 200


def test_status_code_pagina_video_nao_encontrado(resp_video_nao_encontrado):
    assert resp_video_nao_encontrado.status_code == 404


def test_titulo_video(resp, video):
    assert_contains(resp, video.titulo)


def test_conteudo_video(resp):
    assert_contains(resp, '<iframe src="https://player.vimeo.com/video/639324828"')
