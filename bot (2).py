"""
🌍 Nur Travel Bot — Telegram bot for travel agency
Stack:   Python 3.10+ | aiogram 3.x
Install: pip install aiogram
Run:     python bot.py
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart, Command

# ─── SETTINGS ─────────────────────────────────────────────────────────────────
BOT_TOKEN = "8716444560:AAFx0dQhG8VfULDEJJewqU8wX4rNQD6P7cI"
ADMIN_ID   = 1056629641
# ──────────────────────────────────────────────────────────────────────────────

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp  = Dispatcher(storage=MemoryStorage())


# ─── TOUR CATALOG ─────────────────────────────────────────────────────────────
TOURS = {
    # ── Kazakhstan ────────────────────────────────────────────────────────────
    "almaty_eco": {
        "emoji": "🏔️",
        "name": "Almaty Experience 360",
        "country": "🇰🇿 Kazakhstan",
        "duration": "4 days / 3 nights",
        "price": "from $280–300 / person",
        "description": (
            "Eco-business tour around Almaty. Day 1 — city tour, Green Bazaar, Kok-Tobe. "
            "Day 2 — Ile-Alatau National Park, mountain trails. "
            "Day 3 — Charyn Canyon, zipline. "
            "Day 4 — business networking or SPA. "
            "Included: 3–4★ hotel, eco-transport, guide, breakfasts, insurance. "
            "Options: Kazakh cooking masterclass, SPA ($30–100). Group up to 15 people."
        ),
    },
    "charyn": {
        "emoji": "🏜️",
        "name": "Charyn Canyon — Day Trip",
        "country": "🇰🇿 Kazakhstan",
        "duration": "1 day",
        "price": "from $35 / person",
        "description": (
            "One-day trip from Almaty. Comfortable transfer, professional guide. "
            "Hiking through the Valley of Castles, picnic by the Charyn River. Return in the evening."
        ),
    },
    "borovoe": {
        "emoji": "🌲",
        "name": "Burabay — Pearl of Kazakhstan",
        "country": "🇰🇿 Kazakhstan",
        "duration": "3 days / 2 nights",
        "price": "from $200 / person",
        "description": (
            "Shchuchinsk-Burabay resort area. Lakes Burabay, Shchuchye, Katarkol. "
            "Horse riding, fishing, SUP boarding, fresh pine air. "
            "Stay in cozy bungalows on the lakeshore."
        ),
    },
    "aktau": {
        "emoji": "🌊",
        "name": "Aktau — Caspian Sea",
        "country": "🇰🇿 Kazakhstan",
        "duration": "5 days / 4 nights",
        "price": "from $280 / person",
        "description": (
            "Beach holiday on the Caspian Sea. Mangyshlak Plateau, underground mosque Shopan-Ata, "
            "chalk canyons of Bozzhyra. Flight from Almaty ~3 hours. 3★ hotel, breakfasts included."
        ),
    },
    "turkestan": {
        "emoji": "🕌",
        "name": "Turkestan — Spiritual Capital",
        "country": "🇰🇿 Kazakhstan",
        "duration": "2 days / 1 night",
        "price": "from $130 / person",
        "description": (
            "Mausoleum of Khoja Ahmed Yasawi (UNESCO), ancient city of Otrar, "
            "Hazret Sultan Mosque, national entertainment park. "
            "Travel by high-speed train or flight."
        ),
    },
    # ── International ──────────────────────────────────────────────────────────
    "dubai": {
        "emoji": "🇦🇪",
        "name": "Dubai — Luxury of the East",
        "country": "🇦🇪 UAE",
        "duration": "5 nights",
        "price": "from $360 / person",
        "description": (
            "Flight from Almaty ~4.5 hours. 4★ hotel near the Persian Gulf. "
            "Burj Khalifa, desert safari, Dubai Mall, Gold Souk. "
            "Breakfasts included. Visa ~$25 (we handle it)."
        ),
    },
    "turkey": {
        "emoji": "🇹🇷",
        "name": "Turkey — All Inclusive",
        "country": "🇹🇷 Turkey, Antalya",
        "duration": "7 nights",
        "price": "from $480 / person",
        "description": (
            "5★ All Inclusive hotel on the first beachfront line. "
            "Unlimited food, pools, beach, entertainment. "
            "Optional excursions: Pamukkale, Cappadocia. Visa-free for Kazakhstan citizens."
        ),
    },
    "thailand": {
        "emoji": "🇹🇭",
        "name": "Thailand — Exotic Asia",
        "country": "🇹🇭 Thailand",
        "duration": "7 nights",
        "price": "from $550 / person",
        "description": (
            "Phuket or Pattaya — your choice. 4★ hotel, breakfasts. "
            "Phi Phi Islands, Thai massage, night markets. "
            "Visa-free entry up to 30 days for Kazakhstan citizens."
        ),
    },
    "egypt": {
        "emoji": "🇪🇬",
        "name": "Egypt — Pyramids & Red Sea",
        "country": "🇪🇬 Egypt",
        "duration": "7 nights",
        "price": "from $380 / person",
        "description": (
            "Hurghada or Sharm el-Sheikh. 4–5★ All Inclusive hotel. "
            "Coral reefs, snorkeling, excursion to the Pyramids of Giza. "
            "Visa on arrival $25."
        ),
    },
    "georgia": {
        "emoji": "🇬🇪",
        "name": "Georgia — Soul of the Caucasus",
        "country": "🇬🇪 Georgia",
        "duration": "3 nights",
        "price": "from $410 / person",
        "description": (
            "Tbilisi, Mtskheta, Kazbegi or Batumi. "
            "Old Tbilisi, thermal baths, Georgian cuisine and wine. "
            "Flight from Almaty ~3 hours. Visa-free entry."
        ),
    },
    "vietnam": {
        "emoji": "🇻🇳",
        "name": "Vietnam — Land of Contrasts",
        "country": "🇻🇳 Vietnam",
        "duration": "9 nights",
        "price": "from $550 / person",
        "description": (
            "Hanoi, Ha Long Bay, Hoi An, Ho Chi Minh City. 4★ hotel. "
            "Ha Long Bay cruise, rice fields, street food. "
            "Visa-free entry up to 45 days."
        ),
    },
    "bali": {
        "emoji": "🌺",
        "name": "Bali — Island of the Gods",
        "country": "🇮🇩 Indonesia, Bali",
        "duration": "6 nights",
        "price": "from $1,750 / person",
        "description": (
            "Ubud, Seminyak, Kuta. Private villa with pool or 4★ hotel. "
            "Tegalalang rice terraces, Mount Batur, Uluwatu temple, surfing, yoga. "
            "Visa-free entry 30 days."
        ),
    },
}

TOUR_GROUPS = {
    "kz": {
        "label": "🇰🇿 Tours in Kazakhstan",
        "keys": ["almaty_eco", "charyn", "borovoe", "aktau", "turkestan"],
    },
    "abroad": {
        "label": "✈️ International Tours",
        "keys": ["dubai", "turkey", "thailand", "egypt", "georgia", "vietnam", "bali"],
    },
}


# ─── FSM STATES ───────────────────────────────────────────────────────────────
class BookingForm(StatesGroup):
    entering_name  = State()
    entering_phone = State()
    entering_dates = State()
    entering_pax   = State()
    confirming     = State()

class ContactForm(StatesGroup):
    entering_question = State()


# ─── KEYBOARDS ────────────────────────────────────────────────────────────────
def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🌍 Our Tours"),     KeyboardButton(text="📞 Contact Us")],
            [KeyboardButton(text="❓ FAQ"),            KeyboardButton(text="📋 My Bookings")],
            [KeyboardButton(text="🔥 Hot Deals")],
        ],
        resize_keyboard=True,
    )

def tour_groups_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=g["label"], callback_data=f"group:{k}")]
        for k, g in TOUR_GROUPS.items()
    ] + [[InlineKeyboardButton(text="🔙 Back", callback_data="back:main")]])

def tours_list_kb(group_key: str):
    group = TOUR_GROUPS[group_key]
    buttons = [
        [InlineKeyboardButton(
            text=f"{TOURS[k]['emoji']} {TOURS[k]['name']}",
            callback_data=f"tour:{k}"
        )] for k in group["keys"]
    ]
    buttons.append([InlineKeyboardButton(text="🔙 Back to Categories", callback_data="back:groups")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def tour_detail_kb(tour_key: str):
    group_key = next((gk for gk, g in TOUR_GROUPS.items() if tour_key in g["keys"]), "kz")
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Book This Tour", callback_data=f"book:{tour_key}")],
        [InlineKeyboardButton(text="🔙 Back to List",   callback_data=f"group:{group_key}")],
    ])

def share_phone_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Share My Phone Number", request_contact=True)]],
        resize_keyboard=True, one_time_keyboard=True,
    )

def confirm_kb():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Confirm", callback_data="confirm:yes"),
        InlineKeyboardButton(text="✏️ Edit",   callback_data="confirm:no"),
    ]])

def hot_tours_kb():
    hot = ["dubai", "turkey", "egypt", "charyn"]
    buttons = [
        [InlineKeyboardButton(
            text=f"{TOURS[k]['emoji']} {TOURS[k]['name']} — {TOURS[k]['price']}",
            callback_data=f"tour:{k}"
        )] for k in hot
    ]
    buttons.append([InlineKeyboardButton(text="🔙 All Tours", callback_data="back:groups")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# ─── HANDLERS: MAIN MENU ──────────────────────────────────────────────────────

@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        f"✈️ Hello, *{message.from_user.first_name}*! Welcome to *Nur Travel* 🌍\n\n"
        "We'll find the perfect tour for you — across Kazakhstan or abroad.\n\n"
        "Choose an option below 👇",
        parse_mode="Markdown",
        reply_markup=main_menu(),
    )

@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "📋 *Bot Commands:*\n\n"
        "/start — Main menu\n"
        "/tours — Tour catalog\n"
        "/hot — Hot deals\n"
        "/contact — Message our manager\n"
        "/faq — Frequently asked questions\n"
        "/cancel — Cancel current action",
        parse_mode="Markdown",
    )

@dp.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Action cancelled.", reply_markup=main_menu())

@dp.message(Command("tours"))
@dp.message(F.text == "🌍 Our Tours")
async def show_tour_groups(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("🗺 Choose a destination:", reply_markup=tour_groups_kb())

@dp.message(Command("hot"))
@dp.message(F.text == "🔥 Hot Deals")
async def show_hot(message: Message):
    await message.answer(
        "🔥 *Hot Deals Right Now:*\n\nPrices are live — book before they're gone!",
        parse_mode="Markdown",
        reply_markup=hot_tours_kb(),
    )

@dp.message(Command("contact"))
@dp.message(F.text == "📞 Contact Us")
async def contact(message: Message, state: FSMContext):
    await message.answer(
        "💬 Send us your question — our manager will reply shortly:",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(ContactForm.entering_question)

@dp.message(ContactForm.entering_question)
async def forward_question(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("✅ Your question has been sent! We'll get back to you soon 🙂", reply_markup=main_menu())
    await bot.send_message(
        ADMIN_ID,
        f"❓ *New Question from Client*\n\n"
        f"👤 {message.from_user.full_name} (@{message.from_user.username})\n"
        f"🆔 {message.from_user.id}\n\n💬 {message.text}",
        parse_mode="Markdown",
    )

@dp.message(Command("faq"))
@dp.message(F.text == "❓ FAQ")
async def faq(message: Message):
    await message.answer(
        "❓ *Frequently Asked Questions:*\n\n"
        "🔹 *How do I book a tour?*\n"
        "Browse catalog → choose a tour → tap 'Book' → fill in your details.\n\n"
        "🔹 *When will a manager contact me?*\n"
        "Within 30 minutes during business hours (9:00–20:00).\n\n"
        "🔹 *Is installment payment available?*\n"
        "Yes! Up to 12 months interest-free.\n\n"
        "🔹 *Do I need a visa for Turkey, Thailand, or Georgia?*\n"
        "No — Kazakhstan citizens enter visa-free.\n"
        "For UAE — visa ~$25, we handle the application.\n\n"
        "🔹 *Does the price include flights?*\n"
        "Yes, unless stated otherwise.",
        parse_mode="Markdown",
        reply_markup=main_menu(),
    )

@dp.message(F.text == "📋 My Bookings")
async def my_bookings(message: Message):
    await message.answer(
        "📋 To check your booking status — please contact us via '📞 Contact Us'.",
        reply_markup=main_menu(),
    )


# ─── INLINE NAVIGATION ────────────────────────────────────────────────────────

@dp.callback_query(F.data == "back:main")
async def cb_back_main(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text("Use the menu below 👇")
    await call.message.answer("Choose an option:", reply_markup=main_menu())
    await call.answer()

@dp.callback_query(F.data == "back:groups")
async def cb_back_groups(call: CallbackQuery):
    await call.message.edit_text("🗺 Choose a destination:", reply_markup=tour_groups_kb())
    await call.answer()

@dp.callback_query(F.data.startswith("group:"))
async def cb_group(call: CallbackQuery):
    gk = call.data.split(":", 1)[1]
    g  = TOUR_GROUPS[gk]
    await call.message.edit_text(f"{g['label']}\n\nSelect a tour:", reply_markup=tours_list_kb(gk))
    await call.answer()

@dp.callback_query(F.data.startswith("tour:"))
async def cb_tour(call: CallbackQuery):
    tk = call.data.split(":", 1)[1]
    t  = TOURS[tk]
    text = (
        f"{t['emoji']} *{t['name']}*\n\n"
        f"🌍 {t['country']}\n"
        f"📅 {t['duration']}\n"
        f"💰 {t['price']}\n\n"
        f"📝 {t['description']}"
    )
    await call.message.edit_text(text, parse_mode="Markdown", reply_markup=tour_detail_kb(tk))
    await call.answer()


# ─── BOOKING FLOW ─────────────────────────────────────────────────────────────

@dp.callback_query(F.data.startswith("book:"))
async def cb_book(call: CallbackQuery, state: FSMContext):
    tk = call.data.split(":", 1)[1]
    await state.update_data(tour_key=tk, tour_name=TOURS[tk]["name"])
    await call.message.edit_text(
        f"📝 *Booking: {TOURS[tk]['name']}*\n\nStep 1/4: Enter your *full name*:",
        parse_mode="Markdown",
    )
    await state.set_state(BookingForm.entering_name)
    await call.answer()

@dp.message(BookingForm.entering_name)
async def book_name(message: Message, state: FSMContext):
    if len(message.text.strip()) < 2:
        return await message.answer("Please enter a valid name.")
    await state.update_data(name=message.text.strip())
    await message.answer("Step 2/4: Share your phone number:", reply_markup=share_phone_kb())
    await state.set_state(BookingForm.entering_phone)

@dp.message(BookingForm.entering_phone, F.contact)
async def book_phone_c(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await _ask_dates(message, state)

@dp.message(BookingForm.entering_phone)
async def book_phone_t(message: Message, state: FSMContext):
    await state.update_data(phone=message.text.strip())
    await _ask_dates(message, state)

async def _ask_dates(message: Message, state: FSMContext):
    await message.answer(
        "Step 3/4: Enter your *preferred travel dates*\n_(e.g. June 10–17, 2025)_",
        parse_mode="Markdown", reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(BookingForm.entering_dates)

@dp.message(BookingForm.entering_dates)
async def book_dates(message: Message, state: FSMContext):
    await state.update_data(dates=message.text.strip())
    await message.answer("Step 4/4: How many travelers?")
    await state.set_state(BookingForm.entering_pax)

@dp.message(BookingForm.entering_pax)
async def book_pax(message: Message, state: FSMContext):
    await state.update_data(pax=message.text.strip())
    d = await state.get_data()
    await message.answer(
        f"✅ *Please review your booking:*\n\n"
        f"🌍 Tour:      {d['tour_name']}\n"
        f"👤 Name:      {d['name']}\n"
        f"📱 Phone:     {d['phone']}\n"
        f"📅 Dates:     {d['dates']}\n"
        f"👥 Travelers: {d['pax']}",
        parse_mode="Markdown", reply_markup=confirm_kb(),
    )
    await state.set_state(BookingForm.confirming)

@dp.callback_query(F.data == "confirm:yes")
async def book_confirm(call: CallbackQuery, state: FSMContext):
    d = await state.get_data()
    await state.clear()
    await call.message.edit_text(
        "🎉 *Booking Received!*\n\n"
        "Our manager will contact you within 30 minutes.\n"
        "Thank you for choosing *Nur Travel*! 🌍",
        parse_mode="Markdown",
    )
    await call.message.answer("Choose an option:", reply_markup=main_menu())
    try:
        await bot.send_message(
            ADMIN_ID,
            f"🔔 *New Booking!*\n\n"
            f"🌍 Tour:      {d.get('tour_name','—')}\n"
            f"👤 Name:      {d.get('name','—')}\n"
            f"📱 Phone:     {d.get('phone','—')}\n"
            f"📅 Dates:     {d.get('dates','—')}\n"
            f"👥 Travelers: {d.get('pax','—')}\n"
            f"🆔 TG ID:     {call.from_user.id}\n"
            f"👤 Username:  @{call.from_user.username}",
            parse_mode="Markdown",
        )
    except Exception as e:
        logging.warning(f"Admin notify failed: {e}")
    await call.answer()

@dp.callback_query(F.data == "confirm:no")
async def book_cancel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text("✏️ Booking cancelled. Start again via '🌍 Our Tours'.")
    await call.message.answer("Choose an option:", reply_markup=main_menu())
    await call.answer()


# ─── RUN ──────────────────────────────────────────────────────────────────────
async def main():
    print("✈️ Nur Travel Bot is running!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
