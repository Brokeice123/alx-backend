import express from 'express';
import { promisify } from 'util';
import { createClient } from 'redis';


// Creating Express app
const app = express();
const port = 1245;

// Creating Redis client
const redisClient = createClient();


const productList = [
    { itemId: 1, itemName: "Suitcase 250", price: 50, initialAvailableQuantity: 4 },
    { itemId: 2, itemName: "Suitcase 450", price: 100, initialAvailableQuantity: 10 },
    { itemId: 3, itemName: "Suitcase 650", price: 350, initialAvailableQuantity: 2 },
    { itemId: 4, itemName: "Suitcase 1050", price: 550, initialAvailableQuantity: 5 }
];


// Promisify all the Redis functions
const setAsync = promisify(redisClient.set).bind(redisClient);
const getAsync = promisify(redisClient.get).bind(redisClient);

// Function reserving a stock by its itemID
async function reserveStockById(itemId, stock) {
    await setAsync(`item.${itemId}`, stock);
}

// Function getting the reserved stock uing its itemID
async function getCurrentReservedStockById(itemId) {
    const reservedStock = await getAsync(`item.${itemId}`);
    return reservedStock ? parseInt(reservedStock) : 0;
}

//  Automatically parsing the request body 
app.use(express.json());

// Listing all products
app.get('/list_products', (req, res) => {
    res.json(productList.map(product => ({
        itemId: product.itemId,
        itemName: product.itemName,
        price: product.price,
        initialAvailableQuantity: product.initialAvailableQuantity
    })));
});

// Getting product details by itemId
app.get('/list_products/:itemId', async (req, res) => {
    const itemId = parseInt(req.params.itemId);
    const product = productList.find(item => item.itemId === itemId);
    if (!product) {
        return res.status(404).json({ status: "Product not found" });
    }
    const currentQuantity = product.initialAvailableQuantity - await getCurrentReservedStockById(itemId);
    res.json({ ...product, currentQuantity });
});

// Route to reserve a product by itemId
app.get('/reserve_product/:itemId', async (req, res) => {
    const itemId = parseInt(req.params.itemId);
    const product = productList.find(item => item.itemId === itemId);
    if (!product) {
        return res.status(404).json({ status: "Product not found" });
    }
    const currentReservedStock = await getCurrentReservedStockById(itemId);
    if (currentReservedStock >= product.initialAvailableQuantity) {
        return res.json({ status: "Not enough stock available", itemId });
    }
    await reserveStockById(itemId, currentReservedStock + 1);
    res.json({ status: "Reservation confirmed", itemId });
});

// Starting the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});