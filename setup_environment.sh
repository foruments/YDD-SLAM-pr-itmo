#!/bin/bash

echo "=== Установка зависимостей для YDD-SLAM ==="

if [ ! -f /etc/lsb-release ]; then
    echo "Ошибка: Требуется Ubuntu 20.04"
    exit 1
fi

sudo apt-get update
sudo apt-get install -y build-essential cmake git wget unzip
sudo apt-get install -y libeigen3-dev
sudo apt-get install -y libepoxy-dev

echo "Установка OpenCV 4.2.0..."
cd ~
git clone --branch 4.2.0 https://github.com/opencv/opencv.git
git clone --branch 4.2.0 https://github.com/opencv/opencv_contrib.git
cd opencv && mkdir build && cd build
cmake -DOPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_INSTALL_PREFIX=/usr/local ..
make -j$(nproc)
sudo make install
sudo ldconfig

echo "Установка Pangolin..."
cd ~
git clone https://github.com/stevenlovegrove/Pangolin.git
cd Pangolin && mkdir build && cd build
cmake -DBUILD_PANGOLIN_PYTHON=OFF ..
make -j$(nproc)
sudo make install

echo "Загрузка LibTorch 1.11.0..."
cd ~
wget https://download.pytorch.org/libtorch/cpu/libtorch-cxx11-abi-shared-with-deps-1.11.0+cpu.zip
unzip libtorch-cxx11-abi-shared-with-deps-1.11.0+cpu.zip -d /usr/local/

echo "Установка Python зависимостей..."
pip3 install -r requirements.txt

echo "=== Установка завершена ==="
echo "Теперь выполните: cd src/yolo_orb_slam3 && ./build.sh"
