from django.contrib import admin


def configure_admin():
    admin.site.site_header  = 'Library — Admin Panel'
    admin.site.site_title   = 'Library Admin'
    admin.site.index_title  = 'Library Management'