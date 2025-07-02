#!/usr/bin/env python3
import os
import sys
import django

# Configurar Django
sys.path.append('/Users/johnperaltarojas/Desktop/proyecto_final')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proy_clinico.settings')
django.setup()

from applications.security.models import GroupModulePermission, Module
from django.contrib.auth.models import Group

def debug_permisos_completo():
    print("=" * 80)
    print("🔍 DEBUG COMPLETO - VISTA GROUP MODULE PERMISSIONS")
    print("=" * 80)
    
    # 1. Verificar grupos existentes
    print("📊 GRUPOS EXISTENTES:")
    grupos = Group.objects.all().order_by('name')
    for grupo in grupos:
        print(f"  • ID {grupo.id}: {grupo.name}")
    print()
    
    # 2. Verificar GroupModulePermissions existentes
    print("📊 GROUP MODULE PERMISSIONS EXISTENTES:")
    gmps = GroupModulePermission.objects.select_related('group', 'module').prefetch_related('permissions', 'module__permissions').order_by('group__name', 'module__name')
    if gmps.exists():
        for gmp in gmps:
            print(f"  • {gmp.group.name} -> {gmp.module.name} ({gmp.permissions.count()} permisos)")
    else:
        print("  ❌ NO hay GroupModulePermissions")
    print()
    
    # 3. Verificar qué pasa con el queryset de la vista (sin filtros)
    print("📊 QUERYSET SIN FILTROS (como en vista):")
    queryset = GroupModulePermission.objects.select_related('group', 'module').prefetch_related('permissions', 'module__permissions').order_by('group__name', 'module__name')
    print(f"Total registros: {queryset.count()}")
    for gmp in queryset:
        print(f"  • {gmp.group.name} -> {gmp.module.name}")
    print()
    
    # 4. Simular el regroup del template
    print("📊 SIMULACIÓN DEL REGROUP DEL TEMPLATE:")
    from collections import defaultdict
    grouped_permissions = defaultdict(list)
    for gmp in queryset:
        grouped_permissions[gmp.group].append(gmp)
    
    print(f"Grupos encontrados en regroup: {len(grouped_permissions)}")
    for grupo, gmps_del_grupo in grouped_permissions.items():
        print(f"  • {grupo.name} (ID: {grupo.id}): {len(gmps_del_grupo)} módulos")
        for gmp in gmps_del_grupo:
            print(f"    - {gmp.module.name}")
    print()
    
    # 5. Verificar específicamente los grupos problemáticos
    print("📊 VERIFICACIÓN ESPECÍFICA GRUPOS PROBLEMÁTICOS:")
    for nombre_grupo in ['Asistente', 'Médicos', 'Administrador']:
        try:
            grupo = Group.objects.get(name=nombre_grupo)
            gmps_grupo = GroupModulePermission.objects.filter(group=grupo)
            print(f"  • {nombre_grupo} (ID: {grupo.id}): {gmps_grupo.count()} registros GMP")
            for gmp in gmps_grupo:
                print(f"    - {gmp.module.name} ({gmp.permissions.count()} permisos)")
        except Group.DoesNotExist:
            print(f"  ❌ Grupo '{nombre_grupo}' no existe")
    print()
    
    print("=" * 80)

if __name__ == "__main__":
    debug_permisos_completo()
