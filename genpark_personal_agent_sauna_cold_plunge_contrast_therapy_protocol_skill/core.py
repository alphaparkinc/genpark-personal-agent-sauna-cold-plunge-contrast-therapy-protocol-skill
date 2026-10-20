# -*- coding: utf-8 -*-
"""Sauna & Cold Plunge Contrast Therapy Longevity Protocol for GenPark Personal Agent."""
import json
from typing import Dict, Any

class SaunaColdPlungeContrastTherapyProtocol:
    """Deliberate heat and cold exposure, HSP70 and brown adipose tissue (BAT) optimization engine."""

    # Soberg Principle targets: 57 mins heat / 11 mins cold weekly
    WEEKLY_HEAT_TARGET_MINS = 57
    WEEKLY_COLD_TARGET_MINS = 11

    @staticmethod
    def design_contrast_therapy_session(primary_goal: str, hours_since_strength_training: float = 24.0) -> Dict[str, Any]:
        """Compute optimal thermal rounds and cold timing relative to hypertrophy window."""
        # Hypertrophy guard: avoid cold plunge < 4 hours after resistance training (blunts mTOR)
        blunt_risk = hours_since_strength_training < 4.0

        if primary_goal == "cardiovascular_longevity":
            rounds = 3
            sauna_mins = 15
            cold_mins = 2
            end_with = "HEAT"
        elif primary_goal == "acute_dopamine_norepinephrine_boost":
            rounds = 2
            sauna_mins = 12
            cold_mins = 3
            end_with = "COLD"
        else:
            rounds = 3
            sauna_mins = 15
            cold_mins = 3
            end_with = "COLD"

        return {
            "goal": primary_goal,
            "prescribed_rounds": rounds,
            "sauna_temp_celsius": "80°C - 90°C (176°F - 194°F)",
            "sauna_duration_per_round_mins": sauna_mins,
            "cold_plunge_temp_celsius": "10°C - 14°C (50°F - 57°F)",
            "cold_duration_per_round_mins": cold_mins,
            "ending_modality": end_with,
            "hypertrophy_blunting_warning": blunt_risk,
            "soberg_principle": "Ending on cold forces metabolic brown adipose tissue shivering thermogenesis to restore homeothermy." if end_with == "COLD" else "Ending on heat maximizes parasympathetic relaxation and endothelial vasodilation."
        }

    @staticmethod
    def audit_weekly_thermal_dosage(logged_sauna_minutes: int, logged_cold_plunge_minutes: int) -> Dict[str, Any]:
        """Audit cumulative exposure against published clinical thresholds (Laukkanen / Soberg)."""
        heat_pct = round((logged_sauna_minutes / SaunaColdPlungeContrastTherapyProtocol.WEEKLY_HEAT_TARGET_MINS) * 100.0, 1)
        cold_pct = round((logged_cold_plunge_minutes / SaunaColdPlungeContrastTherapyProtocol.WEEKLY_COLD_TARGET_MINS) * 100.0, 1)

        return {
            "weekly_heat_progress": f"{logged_sauna_minutes} / {SaunaColdPlungeContrastTherapyProtocol.WEEKLY_HEAT_TARGET_MINS} mins ({heat_pct}%)",
            "weekly_cold_progress": f"{logged_cold_plunge_minutes} / {SaunaColdPlungeContrastTherapyProtocol.WEEKLY_COLD_TARGET_MINS} mins ({cold_pct}%)",
            "heat_shock_protein_status": "MAXIMAL_INDUCTION" if heat_pct >= 100 else "PARTIAL",
            "norepinephrine_dopamine_baseline": "ELEVATED" if cold_pct >= 100 else "MAINTAINING",
            "all_cause_mortality_benefit": "Accomplishing 4x/week sauna correlates with 40% reduction in all-cause mortality (KIHD Study)."
        }
