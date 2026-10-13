"""
Farm History and Unified Farm Log Page (Module H).
Provides a consolidated chronological history of harvests, health observations, fertilizers, and soil tests.
"""

import pandas as pd
import streamlit as st

from src.ui.components import render_page_header, render_ai_status


def render_farm_history(is_tamil: bool) -> None:
    """Renders the comprehensive farm history and data export page."""
    render_page_header(
        title_en="Farm History & Integrated Logs (Module H)",
        title_ta="பண்ணை வரலாற்றுப் பதிவுகள் மற்றும் மேலாண்மை (பகுதி H)",
        subtitle_en="Review chronological farm management logs, inspect trends, and export dataset records",
        subtitle_ta="அனைத்து பதிவுகளையும் ஒரே இடத்தில் ஆராய்ந்து, தரவுகளைப் பதிவிறக்கம் செய்துகொள்ளுங்கள்",
        is_tamil=is_tamil,
    )

    render_ai_status(
        phase_description_en="Unified Farm Journal Active. In Phase 3, these records will be saved to an ACID-compliant SQLite database file.",
        is_tamil=is_tamil,
    )

    tab_harvest, tab_health, tab_fert, tab_soil, tab_weath = st.tabs([
        "🌸 Flower Harvests" if not is_tamil else "🌸 அறுவடைப் பதிவுகள்",
        "🍃 Plant Health" if not is_tamil else "🍃 பயிர் நலம்",
        "🧪 Fertilizer Logs" if not is_tamil else "🧪 உரப் பதிவுகள்",
        "🔬 Soil Tests" if not is_tamil else "🔬 மண் பரிசோதனை",
        "🌦️ Weather & Irrigation" if not is_tamil else "🌦️ வானிலை & பாசனம்",
    ])

    with tab_harvest:
        st.markdown("### 🌸 Flower Harvest & Staging Observations")
        if st.session_state.harvest_records:
            df_h = pd.DataFrame(st.session_state.harvest_records)
            st.dataframe(df_h, use_container_width=True, hide_index=True)
            csv_h = df_h.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Export Harvest Records (CSV)",
                data=csv_h,
                file_name="jasmine_harvest_records.csv",
                mime="text/csv",
                key="dl_harvest",
            )
        else:
            st.info("No flower harvest records found.")

    with tab_health:
        st.markdown("### 🍃 Plant Health & Damage Observations")
        if st.session_state.plant_health_records:
            df_health = pd.DataFrame(st.session_state.plant_health_records)
            st.dataframe(df_health, use_container_width=True, hide_index=True)
            csv_hl = df_health.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Export Health Records (CSV)",
                data=csv_hl,
                file_name="jasmine_plant_health_records.csv",
                mime="text/csv",
                key="dl_health",
            )
        else:
            st.info("No plant health records found.")

    with tab_fert:
        st.markdown("### 🧪 Fertilizer & Nutrient Applications")
        if st.session_state.fertilizer_records:
            df_f = pd.DataFrame(st.session_state.fertilizer_records)
            st.dataframe(df_f, use_container_width=True, hide_index=True)
            csv_f = df_f.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Export Fertilizer Records (CSV)",
                data=csv_f,
                file_name="jasmine_fertilizer_records.csv",
                mime="text/csv",
                key="dl_fert",
            )
        else:
            st.info("No fertilizer records found.")

    with tab_soil:
        st.markdown("### 🔬 Soil Health Reports")
        if st.session_state.soil_test_records:
            df_s = pd.DataFrame(st.session_state.soil_test_records)
            st.dataframe(df_s, use_container_width=True, hide_index=True)
            csv_s = df_s.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Export Soil Test Records (CSV)",
                data=csv_s,
                file_name="jasmine_soil_tests.csv",
                mime="text/csv",
                key="dl_soil",
            )
        else:
            st.info("No soil test records found.")

    with tab_weath:
        st.markdown("### 🌦️ Weather & Irrigation Logs")
        if st.session_state.weather_irrigation_records:
            df_w = pd.DataFrame(st.session_state.weather_irrigation_records)
            st.dataframe(df_w, use_container_width=True, hide_index=True)
            csv_w = df_w.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Export Weather & Irrigation Logs (CSV)",
                data=csv_w,
                file_name="jasmine_weather_irrigation.csv",
                mime="text/csv",
                key="dl_weath",
            )
        else:
            st.info("No weather or irrigation records found.")
