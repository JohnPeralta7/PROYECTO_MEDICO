from django.urls import path

from applications.security.views.auth import signin, signout
from applications.security.views.menu import MenuCreateView, MenuDeleteView, MenuListView, MenuUpdateView
from applications.security.views.module import ModuleCreateView, ModuleDeleteView, ModuleListView, ModuleUpdateView
from applications.security.views.user import (
    UserListView, UserCreateView, UserUpdateView, UserDeleteView, UserDetailView
)
from applications.security.views.group_module_permission import (
    GroupModulePermissionListView, GroupModulePermissionCreateView, GroupModulePermissionUpdateView, GroupModulePermissionDeleteView
)

app_name='security' # define un espacio de nombre para la aplicacion
urlpatterns = [

  # rutas de modulos
  path('module_list/',ModuleListView.as_view() ,name="module_list"),
  path('module_create/', ModuleCreateView.as_view(),name="module_create"),
  path('module_update/<int:pk>/', ModuleUpdateView.as_view(),name='module_update'),
  path('module_delete/<int:pk>/', ModuleDeleteView.as_view(),name='module_delete'),

# rutas de menus
  path('menu_list/',MenuListView.as_view() ,name="menu_list"),
  path('menu_create/', MenuCreateView.as_view(),name="menu_create"),
  path('menu_update/<int:pk>/', MenuUpdateView.as_view(),name='menu_update'),
  path('menu_delete/<int:pk>/', MenuDeleteView.as_view(),name='menu_delete'),


    # rutas de usuarios
  path('user_list/', UserListView.as_view(), name='user_list'),
  path('user_create/', UserCreateView.as_view(), name='user_create'),
  path('user_update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
  path('user_delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
  path('user_detail/<int:pk>/', UserDetailView.as_view(), name='user_detail'),

  # rutas de grupos-módulos-permisos
  path('group_module_permission_list/', GroupModulePermissionListView.as_view(), name='group_module_permission_list'),
  path('group_module_permission_create/', GroupModulePermissionCreateView.as_view(), name='group_module_permission_create'),
  path('group_module_permission_update/<int:pk>/', GroupModulePermissionUpdateView.as_view(), name='group_module_permission_update'),
  path('group_module_permission_delete/<int:pk>/', GroupModulePermissionDeleteView.as_view(), name='group_module_permission_delete'),

  # rutas de autenticacion
  path('logout/', signout, name='signout'),
  path('signin/', signin, name='signin'),
  #path('signup/', signup, name='signup'),
]


#PILAS PONER LAS URLS DEL PROYECTO ORIGINAL, DEL MOD SEGURIDAD.