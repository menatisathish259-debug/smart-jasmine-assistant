"""
Shared UI Components, Styling, and Agricultural Badges for Streamlit Interface.
"""

import streamlit as st
from config.settings import CROP_NAME_EN, CROP_NAME_TA, CROP_NAME_TE, SOIL_PH_RANGE
from src.core.i18n import normalize_lang


def inject_custom_css() -> None:
    """Injects high-aesthetic, mobile-friendly botanical styling with Tamil & Telugu typography."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Noto+Sans+Tamil:wght@400;600;700&family=Noto+Sans+Telugu:wght@400;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', 'Noto Sans Tamil', 'Noto Sans Telugu', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Top Header Banner */
        .page-header {
            background: linear-gradient(135deg, #081c15 0%, #1b4332 55%, #2d6a4f 100%);
            padding: 1.5rem 1.8rem;
            border-radius: 16px;
            color: #ffffff;
            margin-bottom: 1.5rem;
            box-shadow: 0 8px 24px rgba(8, 28, 21, 0.2);
            border: 1px solid rgba(82, 183, 136, 0.25);
        }

        .page-title {
            font-size: 1.85rem;
            font-weight: 800;
            margin: 0;
            color: #d8f3dc;
            line-height: 1.2;
        }

        .page-subtitle {
            font-size: 0.95rem;
            color: #b7e4c7;
            margin-top: 0.4rem;
            margin-bottom: 0;
        }

        /* Card System */
        .farm-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 1.25rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        }

        .farm-card:hover {
            box-shadow: 0 6px 18px rgba(45, 106, 79, 0.08);
        }

        .metric-tile {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 1rem;
            box-shadow: 0 2px 6px rgba(0,0,0,0.02);
            text-align: left;
        }

        .metric-label {
            font-size: 0.75rem;
            text-transform: uppercase;
            font-weight: 700;
            color: #64748b;
            letter-spacing: 0.5px;
        }

        .metric-value {
            font-size: 1.4rem;
            font-weight: 800;
            color: #1b4332;
            margin: 0.2rem 0;
        }

        .metric-sub {
            font-size: 0.8rem;
            color: #52b788;
            font-weight: 600;
        }

        /* Safety & Truth Banners */
        .safety-banner {
            background: #fffbeb;
            border-left: 4px solid #f59e0b;
            padding: 0.85rem 1.1rem;
            border-radius: 8px;
            margin: 1rem 0;
            color: #92400e;
            font-size: 0.88rem;
        }

        .ai-status-badge {
            display: inline-block;
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            color: #1e40af;
            font-size: 0.8rem;
            font-weight: 600;
            padding: 4px 10px;
            border-radius: 20px;
            margin-bottom: 0.8rem;
        }

        /* Tags */
        .stage-pill {
            display: inline-block;
            font-size: 0.75rem;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 6px;
        }

        .pill-ready { background: #d8f3dc; color: #1b4332; border: 1px solid #95d5b2; }
        .pill-not-ready { background: #faedcd; color: #7f4f24; border: 1px solid #d4a373; }
        .pill-too-open { background: #fde2e4; color: #9d0208; border: 1px solid #f4a261; }
        .pill-damaged { background: #ffe3e3; color: #9b2226; border: 1px solid #e63946; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(
    title_en: str,
    title_ta: str,
    subtitle_en: str,
    subtitle_ta: str,
    is_tamil: bool = False,
    lang: str = "en",
    title_te: str = "",
    subtitle_te: str = "",
) -> None:
    """Renders the top banner for each page in pure single-language script."""
    current_lang = normalize_lang(lang, is_tamil)
    if current_lang == "ta":
        title = title_ta
        subtitle = subtitle_ta
    elif current_lang == "te":
        title = title_te if title_te else title_en
        subtitle = subtitle_te if subtitle_te else subtitle_en
    else:
        title = title_en
        subtitle = subtitle_en

    st.markdown(
        f"""
        <div class="page-header">
            <h1 class="page-title">{title}</h1>
            <p class="page-subtitle">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_safety_warning(
    message_en: str,
    message_ta: str,
    is_tamil: bool = False,
    lang: str = "en",
    message_te: str = "",
) -> None:
    """Renders prominent agricultural safety reminder in pure single-language script."""
    current_lang = normalize_lang(lang, is_tamil)
    if current_lang == "ta":
        prefix = "விவசாய பாதுகாப்பு அறிவிப்பு"
        message = message_ta
    elif current_lang == "te":
        prefix = "వ్యవసాయ భద్రతా సమాచారం"
        message = message_te if message_te else message_en
    else:
        prefix = "Agricultural Safety Notice"
        message = message_en

    st.markdown(
        f"""
        <div class="safety-banner">
            ⚠️ <b>{prefix}:</b> {message}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_ai_status(
    phase_description_en: str,
    is_tamil: bool = False,
    lang: str = "en",
    desc_ta: str = "",
    desc_te: str = "",
) -> None:
    """Renders honest AI status badge in pure single-language script."""
    current_lang = normalize_lang(lang, is_tamil)
    if current_lang == "ta":
        prefix = "செயற்கை நுண்ணறிவு நிலை"
        desc = desc_ta if desc_ta else "களத் தரவு மற்றும் வேளாண் விதிகள் சரிபார்க்கப்பட்டன."
    elif current_lang == "te":
        prefix = "కృత్రిమ మేధస్సు స్థితి"
        desc = desc_te if desc_te else "క్షేత్ర స్థాయి డేటా నమోదు మరియు వ్యవసాయ నియమాలు ధృవీకరించబడ్డాయి."
    else:
        prefix = "AI Status"
        desc = phase_description_en

    st.markdown(
        f"""
        <div class="ai-status-badge">
            🔬 <b>{prefix}:</b> {desc}
        </div>
        """,
        unsafe_allow_html=True,
    )
