from django.shortcuts import render


def video(request, slug):
    videos = {
        'motivacao': {'titulo': 'Video Aperitivo: Motivação', 'vimeo_id': 639324828},
        'instalacao-windows': {'titulo': 'Video Aperitivo: Instalação Windows', 'vimeo_id': 251497668},
    }
    video = videos[slug]
    return render(request, 'aperitivos/video.html', context={'video': video})
