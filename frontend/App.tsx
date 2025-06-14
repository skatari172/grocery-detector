import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import UploadScreen from './screens/UploadScreen';
import ResultScreen from './screens/ResultScreen';

export type RootStackParamList = {
  Upload: undefined;
  Result: { imageUri: string; predictions: any[] };
};

const Stack = createNativeStackNavigator<RootStackParamList>();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Upload">
        <Stack.Screen 
          name="Upload" 
          component={UploadScreen}
          options={{ title: 'Grocery Detector' }}
        />
        <Stack.Screen 
          name="Result" 
          component={ResultScreen}
          options={{ title: 'Detection Results' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
} 