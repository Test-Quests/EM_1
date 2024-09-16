import asyncio
from playwright.async_api import async_playwright


def checking_url(current_url, right_url, error_text):
    assert current_url == right_url, error_text


async def test_run():
    async with async_playwright() as pl:
        chrom = await pl.chromium.launch()
        page = await chrom.new_page()
        await page.goto("https://www.saucedemo.com/")

        await page.get_by_placeholder("Username").fill("standard_user")
        await page.get_by_placeholder("Password").fill("secret_sauce")
        await page.get_by_role("button", name="Login").click()

        checking_url(page.url, 'https://www.saucedemo.com/inventory.html', 'Ошибка при попытке залогиниться')

        await page.click('#add-to-cart-sauce-labs-bolt-t-shirt')
        await page.click('.shopping_cart_link')

        checking_url(page.url, 'https://www.saucedemo.com/cart.html', 'Ошибка, не произошёл переход в корзину ')

        item_name = await page.text_content('.inventory_item_name')
        assert item_name == "Sauce Labs Bolt T-Shirt", "Товар в корзине некорректный"

        await page.click('#checkout')
        checking_url(page.url, "https://www.saucedemo.com/checkout-step-one.html", "Ошибка при попытке начала совершения заказа")

        await page.fill('#first-name', 'Denis')
        await page.fill('#last-name', 'Sidorov')
        await page.fill('#postal-code', '54321')

        await page.click('#continue')
        checking_url(page.url, "https://www.saucedemo.com/checkout-step-two.html", "Ошибка при переходе после на второй этап покупки")

        await page.click('#finish')
        checking_url(page.url, "https://www.saucedemo.com/checkout-complete.html", "Ошибка при переходе на завершающую страницу покупки")

        success_message = await page.text_content('.complete-header')
        assert success_message == "Thank you for your order!", "Ошибка при попытке оформления покупки"

        print("Тест успешно выполнен!")

        await chrom.close()


asyncio.run(test_run())
