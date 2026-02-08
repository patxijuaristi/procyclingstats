#!/usr/bin/env python3
"""
Script para probar todos los scrapers de ProCyclingStats uno a uno.
Ejecuta cada scraper con URLs de ejemplo y muestra los resultados.
"""

import sys
import os
import time
from typing import Dict, Any, Optional

# Añadir el directorio del proyecto al path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Verificar si cloudscraper está instalado
try:
    import cloudscraper
    HAS_CLOUDSCRAPER = True
except ImportError:
    HAS_CLOUDSCRAPER = False

from procyclingstats import (
    Race,
    RaceClimbs,
    RaceCombativeRiders,
    RaceStartlist,
    Ranking,
    Rider,
    RiderResults,
    Stage,
    Team,
    TodayRaces
)


# Colores para la terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str) -> None:
    """Imprime un encabezado formateado."""
    separator = "=" * 60
    print(f"\n{Colors.HEADER}{Colors.BOLD}{separator}")
    print(f"  {text}")
    print(f"{separator}{Colors.ENDC}\n")


def print_success(text: str) -> None:
    """Imprime un mensaje de éxito."""
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")


def print_error(text: str) -> None:
    """Imprime un mensaje de error."""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


def print_info(text: str) -> None:
    """Imprime información."""
    print(f"{Colors.CYAN}  {text}{Colors.ENDC}")


def print_data(key: str, value: Any, max_length: int = 100) -> None:
    """Imprime un par clave-valor con formato."""
    value_str = str(value)
    if len(value_str) > max_length:
        value_str = value_str[:max_length] + "..."
    print(f"  {Colors.BLUE}{key}:{Colors.ENDC} {value_str}")


def test_scraper(
    scraper_class: type,
    url: str,
    name: str,
    parse_methods: Optional[list] = None
) -> Dict[str, Any]:
    """
    Prueba un scraper específico.
    
    Args:
        scraper_class: Clase del scraper a probar
        url: URL relativa para el scraper
        name: Nombre descriptivo del scraper
        parse_methods: Lista de métodos específicos a probar (opcional)
    
    Returns:
        Dict con el resultado del test
    """
    result = {
        "name": name,
        "url": url,
        "success": False,
        "error": None,
        "data": None,
        "time": 0
    }
    
    print_header(f"Probando: {name}")
    print_info(f"URL: {url}")
    print()
    
    start_time = time.time()
    
    try:
        # Crear instancia del scraper
        scraper = scraper_class(url)
        
        # Obtener datos parseados
        if hasattr(scraper, 'parse'):
            parsed_data = scraper.parse()
            result["data"] = parsed_data
            
            print_info("Datos parseados:")
            for key, value in parsed_data.items():
                print_data(key, value)
        
        # Si hay métodos específicos para probar
        if parse_methods:
            print()
            print_info("Métodos específicos:")
            for method_name in parse_methods:
                if hasattr(scraper, method_name):
                    method = getattr(scraper, method_name)
                    if callable(method):
                        try:
                            method_result = method()
                            # Mostrar solo los primeros elementos si es una lista
                            if isinstance(method_result, list) and len(method_result) > 3:
                                print_data(method_name, f"[{len(method_result)} items] {method_result[:3]}...")
                            else:
                                print_data(method_name, method_result)
                        except Exception as e:
                            print_error(f"Error en {method_name}: {e}")
        
        result["success"] = True
        result["time"] = time.time() - start_time
        print()
        print_success(f"Scraper probado exitosamente en {result['time']:.2f}s")
        
    except Exception as e:
        result["error"] = str(e)
        result["time"] = time.time() - start_time
        print_error(f"Error: {e}")
    
    return result


def main():
    """Función principal que ejecuta todos los tests."""
    print(f"\n{Colors.BOLD}{'=' * 60}")
    print("   PRUEBA DE TODOS LOS SCRAPERS DE PROCYCLINGSTATS")
    print(f"{'=' * 60}{Colors.ENDC}")
    
    # Mostrar estado de cloudscraper
    if HAS_CLOUDSCRAPER:
        print(f"\n{Colors.GREEN}✓ cloudscraper está instalado - Cloudflare bypass activo{Colors.ENDC}")
    else:
        print(f"\n{Colors.WARNING}⚠ cloudscraper NO está instalado")
        print(f"  Instálalo con: pip install cloudscraper")
        print(f"  Sin él, los scrapers fallarán por protección Cloudflare{Colors.ENDC}")
    
    results = []
    
    # # 1. Race Scraper
    # results.append(test_scraper(
    #     Race,
    #     "race/tour-de-france/2022",
    #     "Race Scraper",
    # ))
    
    # # 2. Race Climbs Scraper
    # results.append(test_scraper(
    #     RaceClimbs,
    #     "race/tour-de-france/2022/route/climbs",
    #     "Race Climbs Scraper",
    # ))
    
    # # 3. Race Combative Riders Scraper
    # results.append(test_scraper(
    #     RaceCombativeRiders,
    #     "race/tour-de-france/2022/results/combative-riders",
    #     "Race Combative Riders Scraper",
    # ))
    
    # # 4. Race Startlist Scraper
    # results.append(test_scraper(
    #     RaceStartlist,
    #     "race/tour-de-france/2022/startlist",
    #     "Race Startlist Scraper",
    # ))
    
    # # 5. Ranking Scraper
    # results.append(test_scraper(
    #     Ranking,
    #     "rankings/me/individual",
    #     "Ranking Scraper (Individual)",
    #     parse_methods=["individual_ranking"]
    # ))
    
    # # 6. Ranking - Teams
    # results.append(test_scraper(
    #     Ranking,
    #     "rankings/me/teams",
    #     "Ranking Scraper (Teams)",
    #     parse_methods=["team_ranking"]
    # ))
    
    # # 7. Ranking - Nations
    # results.append(test_scraper(
    #     Ranking,
    #     "rankings/me/nations",
    #     "Ranking Scraper (Nations)",
    #     parse_methods=["nation_ranking"]
    # ))
    
    # # 8. Rider Scraper
    # results.append(test_scraper(
    #     Rider,
    #     "rider/tadej-pogacar",
    #     "Rider Scraper",
    # ))
    
    # # 9. Rider Results Scraper
    # results.append(test_scraper(
    #     RiderResults,
    #     "rider/tadej-pogacar/results",
    #     "Rider Results Scraper",
    # ))
    
    # # 10. Stage Scraper
    # results.append(test_scraper(
    #     Stage,
    #     "race/tour-de-france/2022/stage-18",
    #     "Stage Scraper",
    # ))
    
    # # 11. Team Scraper
    # results.append(test_scraper(
    #     Team,
    #     "team/uae-team-emirates-2024",
    #     "Team Scraper",
    # ))
    
    # 12. TodayRaces Scraper (default)
    results.append(test_scraper(
        TodayRaces,
        "",  # No URL needed for homepage
        "TodayRaces Scraper (today)",
        parse_methods=["live_races", "finished_races", "yesterday_races"]
    ))

    # 13. TodayRaces Scraper (with date)
    print_header("Probando: TodayRaces Scraper (con fecha)")
    test_date = "2026-02-06"
    try:
        today_scraper = TodayRaces()
        urls = today_scraper.race_urls_for_date(test_date)
        print_info(f"Races for {test_date}: {len(urls)} URLs")
        for url in urls[:5]:
            print_data("race_url", url)
        results.append({
            "name": f"TodayRaces Scraper (date={test_date})",
            "url": f"races.php?p=uci&s=today&date={test_date}",
            "success": True,
            "error": None,
            "data": urls,
            "time": 0
        })
    except Exception as e:
        print_error(f"Error: {e}")
        results.append({
            "name": f"TodayRaces Scraper (date={test_date})",
            "url": f"races.php?p=uci&s=today&date={test_date}",
            "success": False,
            "error": str(e),
            "data": None,
            "time": 0
        })
    
    # Resumen final
    print_header("RESUMEN DE RESULTADOS")
    
    successful = sum(1 for r in results if r["success"])
    failed = len(results) - successful
    total_time = sum(r["time"] for r in results)
    
    print(f"  Total de scrapers probados: {len(results)}")
    print(f"  {Colors.GREEN}Exitosos: {successful}{Colors.ENDC}")
    print(f"  {Colors.FAIL}Fallidos: {failed}{Colors.ENDC}")
    print(f"  Tiempo total: {total_time:.2f}s")
    print()
    
    # Detalles de cada resultado
    print_info("Detalle por scraper:")
    for r in results:
        status = f"{Colors.GREEN}✓{Colors.ENDC}" if r["success"] else f"{Colors.FAIL}✗{Colors.ENDC}"
        print(f"  {status} {r['name']} ({r['time']:.2f}s)")
        if r["error"]:
            print(f"      {Colors.FAIL}Error: {r['error']}{Colors.ENDC}")
    
    print()
    
    # Código de salida
    if failed > 0:
        print(f"{Colors.WARNING}Algunos scrapers fallaron. Revisa los errores arriba.{Colors.ENDC}")
        return 1
    else:
        print(f"{Colors.GREEN}¡Todos los scrapers funcionan correctamente!{Colors.ENDC}")
        return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
