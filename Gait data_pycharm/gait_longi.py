{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "import time as t\n",
    "\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "import scipy as sp\n",
    "from scipy import stats"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 사용할 변수명\n",
    "\n",
    "cc = [\n",
    "    \"subject\", \"age\", \"group\", \"time\",\n",
    "    \"R_HIP_Flex_ANG\", \"L_HIP_Flex_ANG\",\n",
    "    \"R_KNEE_Flex_ANG\", \"L_KNEE_Flex_ANG\",\n",
    "    \"R_ANK_Flex_ANG\", \"L_ANK_Flex_ANG\",\n",
    "    \"R_Pelvis_Lat_Tilt\", \"L_Pelvis_Lat_Tilt\",\n",
    "    \"R_HIP_Rot_ANG\", \"L_HIP_Rot_ANG\",\n",
    "    \"R_Foot_Orientation\", \"L_Foot_Orientation\"\n",
    "]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "# raw data가 들어있는 폴더명\n",
    "# .(콤마)는 현위치를 의미. 현 위치의 하위 폴더 ./폴더명\n",
    "\n",
    "path_false = \"./data/20190709/\"\n",
    "path_true = \"./data/20190709/\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "# xlsx 파일에서 데이터와 age를 읽어오는 함수\n",
    "\n",
    "def read_files(path, file):\n",
    "    data = pd.read_excel(\n",
    "        os.path.join(path, file),\n",
    "        sheet_name=\"Average\",\n",
    "        header=1,\n",
    "        skiprows=27,)\n",
    "    try:\n",
    "        age = pd.read_excel(\n",
    "            os.path.join(path, file),\n",
    "            skipfooter=17,\n",
    "            header=1,\n",
    "        )[\"Unnamed: 16\"][6]\n",
    "    except Exception as e:\n",
    "        print(file)\n",
    "        age = np.nan\n",
    "    return data, age"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 파일 저장용 함수\n",
    "\n",
    "def save_data(result, group: str = \"all\"):\n",
    "    now = t.localtime()\n",
    "    folder_name = \"result\"\n",
    "    try:\n",
    "        if not(os.path.isdir(folder_name)):\n",
    "            os.makedirs(os.path.join(folder_name))\n",
    "    except OSError as e:\n",
    "        if e.errno != errno.EEXIST:\n",
    "            print(\"Failed to create directory!!!!!\")\n",
    "            raise\n",
    "\n",
    "    s = \"%04d%02d%02d_%02d%02d\" % (now.tm_year, now.tm_mon,\n",
    "                                   now.tm_mday, now.tm_hour, now.tm_min)\n",
    "\n",
    "    # 파일 저장\n",
    "    result.to_csv(\"./{}/gait_{}_{}.csv\".format(folder_name, s, group),\n",
    "                  encoding='cp949', index=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "['245.xls', '414.xls', 'CP_data.xlsx', 'gait_20190208.xlsx']"
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# 파일 읽는 순서 상관 있는지? \n",
    "\n",
    "# key=lambda x: int(x.split(\".\")[0]))\n",
    "files_false = sorted(os.listdir(path_false),)\n",
    "files_false = [f for f in files_false if \".xl\" in f] # 엑셀 파일만 가능하도록\n",
    "files_false"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "245.xls\n",
      "414.xls\n",
      "CPU times: user 5.41 s, sys: 48 ms, total: 5.46 s\n",
      "Wall time: 5.45 s\n"
     ]
    }
   ],
   "source": [
    "%%time\n",
    "\n",
    "# 일반적인 table로 생성 후, 가로로 붙이는 작업을 한다.\n",
    "\n",
    "time = np.arange(1, 101)\n",
    "subject = 0\n",
    "result = pd.DataFrame()\n",
    "\n",
    "for file in files_false:\n",
    "    print(file)\n",
    "    data, age = read_files(path_false, file)\n",
    "    group = 0\n",
    "    data[\"subject\"] = subject\n",
    "    data[\"age\"] = age\n",
    "    data[\"group\"] = group\n",
    "    data[\"time\"] = time\n",
    "    data = data[cc]\n",
    "\n",
    "    if result.empty:\n",
    "        cols = cc\n",
    "        c = cc[3:]\n",
    "\n",
    "        # make colums\n",
    "        col_result = []\n",
    "        for n in range(1, 101):\n",
    "            col_result.extend(list(map(lambda x: x+\"_{:03}\".format(n), c)))\n",
    "        kkk = cols[:3]+col_result\n",
    "        result = pd.DataFrame(columns=kkk)\n",
    "\n",
    "    # make data to longitudinal\n",
    "    longi_data = []\n",
    "    for aa in data[data.columns[3:]].values.tolist():\n",
    "        longi_data.extend(aa)\n",
    "\n",
    "    temp = pd.DataFrame([[subject,  age, group, ] + longi_data], columns=kkk)\n",
    "    result = result.append(temp, ignore_index=True)\n",
    "\n",
    "    subject += 1"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "# save false\n",
    "save_data(result=result, group=\"false\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>subject</th>\n",
       "      <th>age</th>\n",
       "      <th>group</th>\n",
       "      <th>time_001</th>\n",
       "      <th>R_HIP_Flex_ANG_001</th>\n",
       "      <th>L_HIP_Flex_ANG_001</th>\n",
       "      <th>R_KNEE_Flex_ANG_001</th>\n",
       "      <th>L_KNEE_Flex_ANG_001</th>\n",
       "      <th>R_ANK_Flex_ANG_001</th>\n",
       "      <th>L_ANK_Flex_ANG_001</th>\n",
       "      <th>...</th>\n",
       "      <th>R_KNEE_Flex_ANG_100</th>\n",
       "      <th>L_KNEE_Flex_ANG_100</th>\n",
       "      <th>R_ANK_Flex_ANG_100</th>\n",
       "      <th>L_ANK_Flex_ANG_100</th>\n",
       "      <th>R_Pelvis_Lat_Tilt_100</th>\n",
       "      <th>L_Pelvis_Lat_Tilt_100</th>\n",
       "      <th>R_HIP_Rot_ANG_100</th>\n",
       "      <th>L_HIP_Rot_ANG_100</th>\n",
       "      <th>R_Foot_Orientation_100</th>\n",
       "      <th>L_Foot_Orientation_100</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>0</td>\n",
       "      <td>30.824658</td>\n",
       "      <td>0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>34.165666</td>\n",
       "      <td>35.200334</td>\n",
       "      <td>8.822333</td>\n",
       "      <td>7.684333</td>\n",
       "      <td>4.160333</td>\n",
       "      <td>1.784000</td>\n",
       "      <td>...</td>\n",
       "      <td>8.302667</td>\n",
       "      <td>8.771667</td>\n",
       "      <td>5.262667</td>\n",
       "      <td>2.997333</td>\n",
       "      <td>-1.403667</td>\n",
       "      <td>-1.641333</td>\n",
       "      <td>11.934333</td>\n",
       "      <td>4.311667</td>\n",
       "      <td>-9.026666</td>\n",
       "      <td>-11.695667</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>1</td>\n",
       "      <td>18.550685</td>\n",
       "      <td>0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>26.598334</td>\n",
       "      <td>26.719666</td>\n",
       "      <td>10.200667</td>\n",
       "      <td>5.647667</td>\n",
       "      <td>-0.374667</td>\n",
       "      <td>2.095333</td>\n",
       "      <td>...</td>\n",
       "      <td>7.751667</td>\n",
       "      <td>7.108333</td>\n",
       "      <td>0.720667</td>\n",
       "      <td>1.264000</td>\n",
       "      <td>-0.332000</td>\n",
       "      <td>1.567333</td>\n",
       "      <td>1.935333</td>\n",
       "      <td>-1.370000</td>\n",
       "      <td>-6.148000</td>\n",
       "      <td>-14.304000</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>2 rows × 1303 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "  subject        age group  time_001  R_HIP_Flex_ANG_001  L_HIP_Flex_ANG_001  \\\n",
       "0       0  30.824658     0       1.0           34.165666           35.200334   \n",
       "1       1  18.550685     0       1.0           26.598334           26.719666   \n",
       "\n",
       "   R_KNEE_Flex_ANG_001  L_KNEE_Flex_ANG_001  R_ANK_Flex_ANG_001  \\\n",
       "0             8.822333             7.684333            4.160333   \n",
       "1            10.200667             5.647667           -0.374667   \n",
       "\n",
       "   L_ANK_Flex_ANG_001  ...  R_KNEE_Flex_ANG_100  L_KNEE_Flex_ANG_100  \\\n",
       "0            1.784000  ...             8.302667             8.771667   \n",
       "1            2.095333  ...             7.751667             7.108333   \n",
       "\n",
       "   R_ANK_Flex_ANG_100  L_ANK_Flex_ANG_100  R_Pelvis_Lat_Tilt_100  \\\n",
       "0            5.262667            2.997333              -1.403667   \n",
       "1            0.720667            1.264000              -0.332000   \n",
       "\n",
       "   L_Pelvis_Lat_Tilt_100  R_HIP_Rot_ANG_100  L_HIP_Rot_ANG_100  \\\n",
       "0              -1.641333          11.934333           4.311667   \n",
       "1               1.567333           1.935333          -1.370000   \n",
       "\n",
       "   R_Foot_Orientation_100  L_Foot_Orientation_100  \n",
       "0               -9.026666              -11.695667  \n",
       "1               -6.148000              -14.304000  \n",
       "\n",
       "[2 rows x 1303 columns]"
      ]
     },
     "execution_count": 9,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "result"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "['245.xls', '414.xls', 'CP_data.xlsx', 'gait_20190208.xlsx']"
      ]
     },
     "execution_count": 10,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# 파일 읽는 순서 상관 있는지?\n",
    "\n",
    "# key=lambda x: int(x.split(\".\")[0]))\n",
    "files_true = sorted(os.listdir(path_true),)\n",
    "files_true = [f for f in files_true if \".xl\" in f] # 엑셀 파일만 가능하도록\n",
    "files_true"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "245.xls\n",
      "414.xls\n",
      "CPU times: user 5.09 s, sys: 24 ms, total: 5.11 s\n",
      "Wall time: 5.11 s\n"
     ]
    }
   ],
   "source": [
    "%%time\n",
    "\n",
    "time = np.arange(1, 101)\n",
    "\n",
    "result_true = pd.DataFrame()\n",
    "\n",
    "for file in files_true:\n",
    "    print(file)\n",
    "    data, age = read_files(path_true, file)\n",
    "    group = 1\n",
    "    data[\"subject\"] = subject\n",
    "    data[\"age\"] = age\n",
    "    data[\"group\"] = group\n",
    "    data[\"time\"] = time\n",
    "    data = data[cc]\n",
    "    \n",
    "    if result_true.empty:\n",
    "        cols = cc\n",
    "        c = cc[3:]\n",
    "\n",
    "        # make colums\n",
    "        col_result = []\n",
    "        for n in range(1, 101):\n",
    "            col_result.extend(list(map(lambda x: x+\"_{:03}\".format(n), c)))\n",
    "        kkk = cols[:3]+col_result\n",
    "        result_true = pd.DataFrame(columns=kkk)\n",
    "\n",
    "    # make data to longitudinal\n",
    "    longi_data = []\n",
    "    for aa in data[data.columns[3:]].values.tolist():\n",
    "        longi_data.extend(aa)\n",
    "\n",
    "    temp = pd.DataFrame([[subject,  age, group, ] + longi_data], columns=kkk)\n",
    "    result_true = result_true.append(temp, ignore_index=True)\n",
    "\n",
    "    subject += 1"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [],
   "source": [
    "# save True\n",
    "save_data(result=result_true, group=\"true\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [],
   "source": [
    "# merge\n",
    "# time 변수 정수화\n",
    "r = result.append(result_true, ignore_index=True, sort=False)\n",
    "r[[\"time_{:03}\".format(x) for x in range(1, 101)]] = r[[\n",
    "    \"time_{:03}\".format(x) for x in range(1, 101)]].applymap(int)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [],
   "source": [
    "# save All\n",
    "save_data(result=r, group=\"all\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>subject</th>\n",
       "      <th>age</th>\n",
       "      <th>group</th>\n",
       "      <th>time_001</th>\n",
       "      <th>R_HIP_Flex_ANG_001</th>\n",
       "      <th>L_HIP_Flex_ANG_001</th>\n",
       "      <th>R_KNEE_Flex_ANG_001</th>\n",
       "      <th>L_KNEE_Flex_ANG_001</th>\n",
       "      <th>R_ANK_Flex_ANG_001</th>\n",
       "      <th>L_ANK_Flex_ANG_001</th>\n",
       "      <th>...</th>\n",
       "      <th>R_KNEE_Flex_ANG_100</th>\n",
       "      <th>L_KNEE_Flex_ANG_100</th>\n",
       "      <th>R_ANK_Flex_ANG_100</th>\n",
       "      <th>L_ANK_Flex_ANG_100</th>\n",
       "      <th>R_Pelvis_Lat_Tilt_100</th>\n",
       "      <th>L_Pelvis_Lat_Tilt_100</th>\n",
       "      <th>R_HIP_Rot_ANG_100</th>\n",
       "      <th>L_HIP_Rot_ANG_100</th>\n",
       "      <th>R_Foot_Orientation_100</th>\n",
       "      <th>L_Foot_Orientation_100</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>2</td>\n",
       "      <td>30.824658</td>\n",
       "      <td>1</td>\n",
       "      <td>1.0</td>\n",
       "      <td>34.165666</td>\n",
       "      <td>35.200334</td>\n",
       "      <td>8.822333</td>\n",
       "      <td>7.684333</td>\n",
       "      <td>4.160333</td>\n",
       "      <td>1.784000</td>\n",
       "      <td>...</td>\n",
       "      <td>8.302667</td>\n",
       "      <td>8.771667</td>\n",
       "      <td>5.262667</td>\n",
       "      <td>2.997333</td>\n",
       "      <td>-1.403667</td>\n",
       "      <td>-1.641333</td>\n",
       "      <td>11.934333</td>\n",
       "      <td>4.311667</td>\n",
       "      <td>-9.026666</td>\n",
       "      <td>-11.695667</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>3</td>\n",
       "      <td>18.550685</td>\n",
       "      <td>1</td>\n",
       "      <td>1.0</td>\n",
       "      <td>26.598334</td>\n",
       "      <td>26.719666</td>\n",
       "      <td>10.200667</td>\n",
       "      <td>5.647667</td>\n",
       "      <td>-0.374667</td>\n",
       "      <td>2.095333</td>\n",
       "      <td>...</td>\n",
       "      <td>7.751667</td>\n",
       "      <td>7.108333</td>\n",
       "      <td>0.720667</td>\n",
       "      <td>1.264000</td>\n",
       "      <td>-0.332000</td>\n",
       "      <td>1.567333</td>\n",
       "      <td>1.935333</td>\n",
       "      <td>-1.370000</td>\n",
       "      <td>-6.148000</td>\n",
       "      <td>-14.304000</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>2 rows × 1303 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "  subject        age group  time_001  R_HIP_Flex_ANG_001  L_HIP_Flex_ANG_001  \\\n",
       "0       2  30.824658     1       1.0           34.165666           35.200334   \n",
       "1       3  18.550685     1       1.0           26.598334           26.719666   \n",
       "\n",
       "   R_KNEE_Flex_ANG_001  L_KNEE_Flex_ANG_001  R_ANK_Flex_ANG_001  \\\n",
       "0             8.822333             7.684333            4.160333   \n",
       "1            10.200667             5.647667           -0.374667   \n",
       "\n",
       "   L_ANK_Flex_ANG_001  ...  R_KNEE_Flex_ANG_100  L_KNEE_Flex_ANG_100  \\\n",
       "0            1.784000  ...             8.302667             8.771667   \n",
       "1            2.095333  ...             7.751667             7.108333   \n",
       "\n",
       "   R_ANK_Flex_ANG_100  L_ANK_Flex_ANG_100  R_Pelvis_Lat_Tilt_100  \\\n",
       "0            5.262667            2.997333              -1.403667   \n",
       "1            0.720667            1.264000              -0.332000   \n",
       "\n",
       "   L_Pelvis_Lat_Tilt_100  R_HIP_Rot_ANG_100  L_HIP_Rot_ANG_100  \\\n",
       "0              -1.641333          11.934333           4.311667   \n",
       "1               1.567333           1.935333          -1.370000   \n",
       "\n",
       "   R_Foot_Orientation_100  L_Foot_Orientation_100  \n",
       "0               -9.026666              -11.695667  \n",
       "1               -6.148000              -14.304000  \n",
       "\n",
       "[2 rows x 1303 columns]"
      ]
     },
     "execution_count": 15,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "result_true[:3]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.5.2"
  },
  "latex_envs": {
   "LaTeX_envs_menu_present": true,
   "autoclose": false,
   "autocomplete": true,
   "bibliofile": "biblio.bib",
   "cite_by": "apalike",
   "current_citInitial": 1,
   "eqLabelWithNumbers": true,
   "eqNumInitial": 1,
   "hotkeys": {
    "equation": "Ctrl-E",
    "itemize": "Ctrl-I"
   },
   "labels_anchors": false,
   "latex_user_defs": false,
   "report_style_numbering": false,
   "user_envs_cfg": false
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
