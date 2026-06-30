'''
script para organizar os arquivos entre treino e teste
'''

import os, random, shutil

# Configurações de caminhos
img_dir = 'data/images'
lbl_dir = 'data/labels'
train_pct = 0.80 

# Verificar se as pastas existem
if not os.path.exists(img_dir):
    print(f"❌ Erro: A pasta '{img_dir}' não foi encontrada no diretório atual!")
    print(f"Diretório atual é: {os.getcwd()}")
    exit()

# Listar arquivos
imagens = [f for f in os.listdir(img_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

print(f"🔍 Total de imagens encontradas para processar: {len(imagens)}")

if len(imagens) == 0:
    print("⚠️ Nenhuma imagem foi encontrada. Verifique a extensão dos arquivos (ex: .jpg ou .JPG).")
    exit()

# Criar a estrutura do YOLO
for folder in ['train/images', 'train/labels', 'val/images', 'val/labels']:
    os.makedirs(folder, exist_ok=True)

random.shuffle(imagens)
split_idx = int(len(imagens) * train_pct)
train_imgs = imagens[:split_idx]
val_imgs = imagens[split_idx:]

def mover_arquivos(lista_imagens, destino):
    contagem = 0
    for img in lista_imagens:
        base_name = os.path.splitext(img)[0]
        lbl = base_name + '.txt'
        
        if os.path.exists(os.path.join(img_dir, img)):
            shutil.move(os.path.join(img_dir, img), os.path.join(f'{destino}/images', img))
            contagem += 1
        if os.path.exists(os.path.join(lbl_dir, lbl)):
            shutil.move(os.path.join(lbl_dir, lbl), os.path.join(f'{destino}/labels', lbl))
    print(f"✅ Movidas {contagem} imagens para '{destino}'")

mover_arquivos(train_imgs, 'train')
mover_arquivos(val_imgs, 'val')
print("🎉 Processo concluído com sucesso!")