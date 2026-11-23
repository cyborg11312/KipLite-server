import asyncio
import os
import websockets

client_connessi = set()

async def gestisci_client(websocket):
    client_connessi.add(websocket)
    try:
        async for messaggio in websocket:
            for client in client_connessi.copy():
                if client != websocket:
                    try:
                        await client.send(messaggio)
                    except:
                        client_connessi.discard(client)
    except:
        pass
    finally:
        client_connessi.discard(websocket)

async def main():
    # Render assegna automaticamente una porta tramite la variabile d'ambiente PORT
    port = int(os.environ.get("PORT", 10000))
    async with websockets.serve(gestisci_client, "0.0.0.0", port):
        print(f"Server KipLite avviato sulla porta {port}...")
        await asyncio.Future()  # Mantiene il server attivo all'infinito

if __name__ == "__main__":
    asyncio.run(main())
